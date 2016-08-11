# -*- coding: utf-8 -*-
'''
try:
    from logger import *
    from joystick import *
    from odometry import *
    from laser import *
except:
    print ('no driver found')
'''
from socket import *
import speech
import threading, platform, copy, time, ConfigParser, os, math

import sys; [sys.path.append( i ) for i in ['..', '../msg', './msg']]
from Node import *
import stdmsg



def create_thread(task):
    if callable(task):
        thread = threading.Thread(target = task)
        thread.setDaemon(True)
        thread.start()
        return thread
    else:
        raise 'task must be callable'
class TTS:
    tts = ""
    status = False
    def speak(self):
        self.status = True
        speech.say(self.tts)
        self.status = False
spk = TTS()
class Driver:
    log_flag = False
    
    cmd_annotation = ""
    last_cmd_time = time.time()

    cmd_lock = threading.RLock()
    cmd_v = 0; cmd_w = 0; cmd_manual = False

    odom_lock = threading.RLock()
    kinect_lock = threading.RLock()
    scan_lock = threading.RLock()
    num = 1
    follow_num=1
    len = 10
    flag = True
    route_flag = True
    pass_flag = False
    follow_flag = False
    follow_flag_1 =False
    relative_pos = stdmsg.Pose()
    global_pos =stdmsg.Pose()   
    last_relative_pos = stdmsg.Pose()
    last_target_pos = stdmsg.Pose()
    goal0 = stdmsg.Pose()
    goal1 =stdmsg.Pose()
    goal2 =stdmsg.Pose()
    goal3 =stdmsg.Pose()
    last_goal_flag = False
    counter=0

    goal_reached_flag = True
    last_goal_reached_flag = True

    def __init__(self):
        self.nh = Node( "tcp://127.0.0.1:5779" )

        #context = zmq.Context(1)
        #self.client = context.socket(zmq.REQ)
        #self.client.connect("tcp://localhost:6100")
        
        #rpc client
        HOS = "127.0.0.1"
        PORT_RPC = '9000'
        self.rpc = RPC()
        self.rpc.connect("tcp://"+HOS+":"+PORT_RPC)

        self.nh.connect("tcp://localhost:9001")
        self.nh.connect("tcp://localhost:9002")
        self.nh.connect("tcp://localhost:8888")
        self.nh.subscrible('msg', self.receive_msg)
        self.nh.subscrible('global_plan',self.PlanHandler)
        self.nh.subscrible('laser',self.ScanHandler)
        self.nh.subscrible('Kinect_Topic',self.Kinect_Process)
        #self._bind_service()

        self._start_hardware()
    def __del__(self):
        self._end_hardware()
        self._unconnect_()


    def _bind_service(self):
        self.context = zmq.Context(1)
        self.server = self.context.socket(zmq.REP)
        self.server.bind( self.service_address )
        self.poll = zmq.Poller()
        self.poll.register(self.server, zmq.POLLIN)
        self.service_buffer = ''

    def _unconnect_(self):
        self.server.close()
        self.context.term()
    def recv(self, timeout):
        sockets = dict(self.poll.poll(timeout*1000))
        if self.server in sockets:
            if sockets[self.server] != zmq.POLLIN:
                return None
        else:
            return None
        return self.server.recv()
        '''if self.service_buffer.find('__end__')>0:
            data = self.service_buffer.split('__end__',2)
            self.service_buffer = data[-1]
            return data[0]'''
    def send(self, data):
        self.server.send(data)

    def _start_hardware(self):

        self.is_running = True
        #self.joy_thread = create_thread(self._joystick)
        self.route_thread = create_thread(self._route)
        self.follow_thread = create_thread(self._follow)
    def _end_hardware(self):
        self.is_running = False
        self.joy_thread.join(1000)
    

    def _route(self):
        while True:
            if self.pass_flag == False and self.num == 2:
                pass
                #print "hhhhhhh"
                #self.num = 2
                #self.flag = True
                #self.num = self.num + 1
                #time.sleep(0.1)
                #self.client.send('set_goal %f %f %f'%(28.194353,13.681081,-0.549720))#2
                
                #self.client.recv()
    def _follow(self):

        speech.say('If you want me to follow you, please tell me')
        listenlist=['please follow me']
        '''
        while True:
            command = speech.input('start command:', listenlist)
            print command
            break
        '''
        self.goal0.position.x=self.global_pos.position.x
        self.goal0.position.y=self.global_pos.position.y
        self.goal0.orentation.yaw=self.global_pos.orentation.yaw
        self.follow_flag = True

        while True:
            with self.kinect_lock:
                #print 'follow_flag:::::::::::::: ',self.follow_flag,'   self.num::::: ',self.num
                if self.follow_flag == True:
                    #self.follow_flag = False
                    pos = stdmsg.Pose()
                    if self.relative_pos.position.x > 0 and self.global_pos.position.x:
                        self.last_relative_pos.position.y = self.relative_pos.position.y
                        
                        self.counter=0
                        theta=math.atan(self.relative_pos.position.y/self.relative_pos.position.x)
                        distance=math.sqrt(self.relative_pos.position.x*self.relative_pos.position.x+self.relative_pos.position.y*self.relative_pos.position.y)
                        #print 'distance::::::::::::::',distance
                        x=(distance)*math.cos(theta)
                        y=(distance)*math.sin(theta)
                        target_pos = stdmsg.Pose()
                        
                        #target_pos.position.x = self.global_pos.position.x + x*math.cos(target_pos.orentation.yaw) - y*math.sin(target_pos.orentation.yaw)
                        #target_pos.position.y = self.global_pos.position.y + x*math.sin(target_pos.orentation.yaw) + y*math.cos(target_pos.orentation.yaw)
                        

                        target_pos.orentation.yaw = self.global_pos.orentation.yaw+theta
                        if(target_pos.orentation.yaw>math.pi):
                            target_pos.orentation.yaw-=2*math.pi
                        elif(target_pos.orentation.yaw<-math.pi):
                            target_pos.orentation.yaw+=2*math.pi
                        
                        target_pos.position.x = self.global_pos.position.x+(distance-1)*math.cos(target_pos.orentation.yaw)
                        target_pos.position.y = self.global_pos.position.y+(distance-1)*math.sin(target_pos.orentation.yaw)
                        #print 'relative_pos:',self.relative_pos.position.x,'\t',self.relative_pos.position.y
                        #print 'theta:',theta
                        #print 'global_pos:',self.global_pos.position.x,'\t',self.global_pos.position.y,'\t',self.global_pos.orentation.yaw
                        #print 'target_pos:',target_pos.position.x,'\t',target_pos.position.y,'\t',target_pos.orentation.yaw
                        if distance<1.5:
                            #print 'Too close,just rotate!!!!!!!!!!!!!!!!!!!!'
                            pos.position.x = self.global_pos.position.x
                            pos.position.y = self.global_pos.position.y
                            pos.orentation.yaw = target_pos.orentation.yaw
                            if(self.rpc!= None):self.rpc.call('set_goal', pos )

                        else:
                            pos.position.x = target_pos.position.x
                            pos.position.y = target_pos.position.y
                            pos.orentation.yaw = target_pos.orentation.yaw
                            if(self.rpc!= None):self.rpc.call('set_goal', pos )

                        
                        self.last_target_pos = target_pos
                    
                    elif self.relative_pos.position.x == 0 and self.global_pos.position.x:
                        if self.counter < 10:
                            pos.position.x = self.last_target_pos.position.x
                            pos.position.y = self.last_target_pos.position.y
                            pos.orentation.yaw = self.last_target_pos.orentation.yaw
                            if(self.rpc!= None):self.rpc.call('set_goal', pos )

                            self.counter+=1

                            time.sleep(15)

                            print 'This is the XuMing Process...'

                        elif self.last_relative_pos.position.y>=0:
                            print 'no target'
                            pos.position.x = self.global_pos.position.x
                            pos.position.y = self.global_pos.position.y
                            pos.orentation.yaw = self.global_pos.orentation.yaw+0.6
                            if(self.rpc!= None):self.rpc.call('set_goal', pos )

                        else:
                            print 'no target'
                            pos.position.x = self.global_pos.position.x
                            pos.position.y = self.global_pos.position.y
                            pos.orentation.yaw = self.global_pos.orentation.yaw-0.6
                            if(self.rpc!= None):self.rpc.call('set_goal', pos )
            

                else:
                    if self.follow_num==1:
                        print 11111111111111
                        pos.position.x = self.goal3.position.x
                        pos.position.y = self.goal3.position.y
                        pos.orentation.yaw = self.goal3.orentation.yaw
                        if(self.rpc!= None):self.rpc.call('set_goal', pos )
            
                    elif self.follow_num==2:
                        print 222222222222222
                        pos.position.x = self.goal2.position.x
                        pos.position.y = self.goal2.position.y
                        pos.orentation.yaw = self.goal2.orentation.yaw
                        if(self.rpc!= None):self.rpc.call('set_goal', pos )

                        '''

                    elif self.follow_num==3:
                        print 33333333333333333
                        pos.position.x = self.goal1.position.x
                        pos.position.y = self.goal1.position.y
                        pos.orentation.yaw = self.goal1.orentation.yaw
                        if(self.rpc!= None):self.rpc.call('set_goal', pos )
                        '''

                    elif self.follow_num==4:
                        pos.position.x = 22.940
                        pos.position.y = 25.98
                        pos.orentation.yaw = 0.05
                        if(self.rpc!= None):self.rpc.call('set_goal', pos )
                        speech.say('star ponit')
                    
                    
            time.sleep(0.15)

    def _joystick(self):

        while True:
            if self.flag == True:
                self.flag = False
                print "self.num=",self.num
                if self.num == 1:
                    self.client.send('set_goal %f %f %f'%(34.373,26.394,0.010))#wp1
                    print "set"
                    self.client.recv()
                elif self.num == 2:
                    #self.num+=1
                    if self.pass_flag == False:
                        self.client.send('set_goal %f %f %f'%(30.030,30.311,3.115))#wp2
                        self.client.recv()
                        self.num = 7
                    else:
                        self.client.send('set_goal %f %f %f'%(30.030,30.311,3.115))#wp2
                        self.client.recv()
                        self.num = 7
                elif self.num == 4:
                    self.client.send('set_goal %f %f %f'%(38.641,27.841,-0.405))#3
                    self.client.recv()
                elif self.num == 5:
                    self.client.send('set_goal %f %f %f'%(37.690,25.940,0.003))#
                    self.client.recv()
                elif self.num == 6:
                    print "555555555555"
                    self.client.send('set_goal %f %f %f'%(18.743,34.158081,-1.222))#18.743,34.158081,-1.222
                    self.client.recv()
                elif self.num == 7:
                    self.client.send('set_goal %f %f %f'%(19.643,30.088081,-2.628))#6
                    self.client.recv()
                elif self.num == 8:
                    self.client.send('set_goal %f %f %f'%(34.586,29.345,0.072))#wp311
                    self.client.recv()
                elif self.num == 9:
                    self.client.send('set_goal %f %f %f'%(34.586,29.345,0.072))#wp3
                    self.client.recv()
                elif self.num == 11 and self.follow_flag == False:
                    speech.say("Bye Bye, I will go back to the last location.")
                    self.client.send('set_goal %f %f %f'%(34.586,29.345,0.072))#wp3
                    self.client.recv()
                    self.follow_flag_1 = False
                    self.num+=1
                elif self.num == 13:
                    self.client.send('set_goal %f %f %f'%(36.850,32.630,1.554))#wp4
                    self.client.recv()

    def run(self, timeout = -1):
        self.nh.run(timeout)
    def ok(self):
        return self.is_running

    @msg_callback(stdmsg.String)
    def receive_msg(self, msg):
        print msg.annotation
        if self.num == 1 or self.num == 7 or self.num == 12:
            pass
        #    speech.say("i have arrived")
        elif self.num == 7:
        #    speech.say("i see you, please stand by!")
            pass
        if self.num == 9:
            speech.say("Hello,I will follow you,if you do not want me to follow, please raise both of your hands over head for two seconds.")
        if self.follow_flag == False and self.follow_flag_1 == False:
            self.num +=1
            self.flag = True
        if self.num == 10:
            self.follow_flag = True
            self.follow_flag_1 = True
            self.num +=1
        if self.follow_flag == False:
            self.follow_num+=1
    @msg_callback(stdmsg.Global_Plan)
    def PlanHandler(self,plan):
        self.len = len(plan.path)
        #print self.len
        if self.len == 0:
            self.route_flag = False
            #print 000000
        else:
            self.route_flag = True
            #print 111111

        self.goal_reached_flag = plan.goal_reached

        #print "follow_flag: ",self.follow_flag
        #print "goal_reached: ",self.goal_reached_flag
        if self.last_goal_reached_flag == False and self.goal_reached_flag == True and self.follow_flag == False:
            print "follow_num: ",self.follow_num
            self.follow_num+=1    

        self.last_goal_reached_flag = plan.goal_reached
        
            

    @msg_callback(stdmsg.Laser_Scan)
    def ScanHandler(self,scan):
        with self.scan_lock:
            #print scan.ranges[int(len(scan.ranges)/2)]
            if scan.ranges[int(len(scan.ranges)/2)] < 1.2:
                #print scan.ranges[int(len(scan.ranges)/2)]
                self.pass_flag = False 
            else: 
                self.pass_flag = True
            #print 'pass_flag:::::', self.pass_flag
            self.global_pos.position.x=scan.robot.position.x
            self.global_pos.position.y=scan.robot.position.y
            self.global_pos.orentation.yaw=scan.robot.orentation.yaw
            #print 'global_pos:',self.global_pos.position.x,'\t',self.global_pos.position.y,'\t',self.global_pos.orentation.yaw
    @msg_callback(stdmsg.Kinect_Msg)
    def Kinect_Process(self, msg):
        #print msg.pos.x,'\t',msg.pos.y,'\t',msg.pos.z,'\t',msg.track_num
        self.relative_pos.position.x=msg.pos.z*1
        self.relative_pos.position.y=msg.pos.x
        distance=math.sqrt(self.relative_pos.position.x*self.relative_pos.position.x+self.relative_pos.position.y*self.relative_pos.position.y)
        #print 'DISTANCE9999999999999999999999999:',distance
        
        if msg.stop_flag == True and self.follow_flag == True:
            self.follow_flag = False
            self.flag = True

        

        if msg.goal_flag == True and self.last_goal_flag == False and self.follow_num== 3:
            self.goal3.position.x=self.global_pos.position.x
            self.goal3.position.y=self.global_pos.position.y
            self.goal3.orentation.yaw=self.global_pos.orentation.yaw
            self.follow_num=0
            print 'goal3_pos:',self.goal3.position.x,'\t',self.goal3.position.y,'\t',self.goal3.orentation.yaw

        
            

        elif msg.goal_flag == True and self.last_goal_flag == False and self.follow_num== 2:
            self.goal2.position.x=self.global_pos.position.x
            self.goal2.position.y=self.global_pos.position.y
            self.goal2.orentation.yaw=self.global_pos.orentation.yaw
            self.follow_num=3
            print 'goal2_pos:',self.goal2.position.x,'\t',self.goal2.position.y,'\t',self.goal2.orentation.yaw
            speech.say("ok i will waiting")

            time.sleep(15)

            speech.say("i will start")

        elif msg.goal_flag == True and self.last_goal_flag == False and self.follow_num== 1:
            self.goal1.position.x=self.global_pos.position.x
            self.goal1.position.y=self.global_pos.position.y
            self.goal1.orentation.yaw=self.global_pos.orentation.yaw
            self.follow_num=2
            print 'goal1_pos:',self.goal1.position.x,'\t',self.goal1.position.y,'\t',self.goal1.orentation.yaw
            
            speech.say("i will waiting")

            time.sleep(15)

            speech.say("i will start")


        elif msg.goal_flag == True and self.last_goal_flag == False and self.follow_num== 0:
            self.follow_num = 1
            self.follow_flag = False

        self.last_goal_flag=msg.goal_flag;




if __name__ == '__main__':

    driver = Driver()

    
    try:
        while driver.ok():
            driver.run(1)
    except KeyboardInterrupt:
        del driver
        print('exit')
    
