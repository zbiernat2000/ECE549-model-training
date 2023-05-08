#include "ros/ros.h"
#include "geometry_msgs/Twist.h"
#include "std_msgs/String.h"
#include "string.h"

ros::Publisher pub;
std::string gesture = "";
//so i dont have to cast types
std::string forward = "forward";
std::string backward = "backward";
std::string left = "left";
std::string right = "right";
geometry_msgs::Twist makeTwist(int x,int z){
/**
creates twistMsg with x and z set
x is forward/back
z is left/right
*/
    geometry_msgs::Twist twistMsg;
    twistMsg.linear.x = x;   //Linear Values
    twistMsg.linear.y = 0;
    twistMsg.linear.z = 0;
    twistMsg.angular.x = 0;  //Angular Values
    twistMsg.angular.y = 0;  
    twistMsg.angular.z = z;

    return twistMsg;
}



//Calculate Loop Stop Time
ros::Time getEndTime(double dur){
/*
calcuates how long to move robot for
*/
  ros::Time startTime = ros::Time::now();
  ros::Duration seconds = ros::Duration(dur);
  ros::Time endTime = startTime + seconds;
  return endTime;
}
void move(double dur,int x, int z){
/**
moves robot for dur seconds, in (x,z) direction
*/
	  geometry_msgs::Twist twistMsg = makeTwist(x,z);
	  ros::Time endTime = getEndTime(dur);
	  while (ros::Time::now() < endTime)
	  {
	    pub.publish(twistMsg);
	    ros::Duration(.01).sleep();
	  }
}

void move2(double x, double z){

	  geometry_msgs::Twist twistMsg = makeTwist(x,z);
	  pub.publish(twistMsg);
	  ros::Duration(.01).sleep();
}

void turn(int z){
/**
backs up robtot then moves robot in z direction
*/
	  //move(1.0, -1, 0);
	  move(.1, 0, z);
}

void get_str(const std_msgs::String::ConstPtr& msg)
{
 gesture = msg->data; //save string

}

int main(int argc, char **argv)
{
  const double turnTime = 1.5;    //When roomba rotates
  ros::init(argc, argv, "example1_a");
  ros::NodeHandle n;
  ros::Subscriber sub2 = n.subscribe("chatter", 1, get_str);
  pub = n.advertise<geometry_msgs::Twist>("cmd_vel", 1); 
  
  while(true)
  {
    ros::spinOnce();
  //check the gesture then move accordingly
  if(forward.compare(gesture) == 0){
	move(.1,1,0);
    }
   else if(right.compare(gesture) == 0){
	turn(-1);
  }
  else if(left.compare(gesture) == 0){
	turn(1);
}
  else if(backward.compare(gesture) == 0){
	move(.1,-1,0);
  }
else
	move(.1,0,0);
}
  return 0;
}
