import logging
import sys
import picar
import cv2
import matplotlib.pyplot as plt


class DeepPiCar(object):

    _DEBUG = False
    _DEBUG_INFO = 'DEBUG "back_wheels.py":'
    
    __INITIAL_SPEED = 0
    __SCREEN_WIDTH = 320
    __SCREEN_HEIGHT = 240

    def __init__(self, debug=False):
        ''' Init camera and wheels'''
        logging.info('Creating a DeepPiCar...')
        
        picar.setup()

        logging.debug('Set up camera')
        self.camera = cv2.VideoCapture(-1)
        self.camera.set(3, self.__SCREEN_WIDTH)
        self.camera.set(4, self.__SCREEN_HEIGHT)
        
        self.pan_servo = picar.Servo.Servo(1)
        self.pan_servo.offset = -30  # calibrate servo to center
        self.pan_servo.write(90)
        
        self.tilt_servo = picar.Servo.Servo(2)
        self.tilt_servo.offset = 40  # calibrate servo to center
        self.tilt_servo.write(90)
        
        logging.debug('Set up back wheels')
        self.back_wheels = picar.back_wheels.Back_Wheels()
        self.back_wheels.speed = 0  #  Speed Range is 0 (stop) - 100 (fastest)

        logging.debug('Set up front wheels')
        self.front_wheels = picar.front_wheels.Front_Wheels()
        self.front_wheels.turning_offset = -20 #  calibrate servo to center
        self.front_wheels.turn(90) #  Steering Range is 45 (left) - 90 (center) - 135 (right) 
        
        logging.info('Created a DeepPiCar')
    
    def __enter__ (self):
        ''' Entering a with statement '''
        return self
        
    def __exit__ (self, type, value, traceback):
        ''' Exit a with statement'''
        if traceback is None:
            # No exception
            logging.info('Exiting with statement normally ')
        else:
            # Exception occurred:
            logging.error('Exiting with statement normally %s' % (traceback))
            
        self.cleanup()
            
    def cleanup(self):
        ''' Reset the hardware'''
        logging.info('Stopping the car, resetting hardware.')
        self.back_wheels.speed = 0
        self.front_wheels.turn(90)
        self.camera.release()
        cv2.destroyAllWindows()
        
    def drive(self, speed = __INITIAL_SPEED):
        ''' Main entry point of the car, and put it in drive mode
        
        Keyword arguments:
        speed -- speed of back wheel, range is 0 (stop) - 100 (fastest)
        '''
        
        logging.info('Starting to drive at speed %s...' % speed)
        self.back_wheels.speed = speed
        while( self.camera.isOpened()):
            _, image = self.camera.read()
            cv2.imshow('Dash Cam', image)
            #plt.imshow(image, shape=(self.__SCREEN_WIDTH * 2, self.__SCREEN_WIDTH*2))
            #plt.show()
            
            if cv2.waitKey(1) & 0xFF == ord('q') :
                self.cleanup()
                break

def test():
        with DeepPiCar() as car:
            car.drive(20)
        
    
if __name__ == '__main__':
    test()