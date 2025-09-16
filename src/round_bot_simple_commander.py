import rclpy
from nav2_simple_commander.robot_navigator import BasicNavigator
from geometry_msgs.msg import PoseStamped
import tf_transformations

def create_pose_stamped(navigator: BasicNavigator, position_x, position_y, orientation_z):
  q_x, q_y, q_z, q_w = tf_transformations.quaternion_from_euler(0.0, 0.0, orientation_z)
  pose =  PoseStamped()
  pose.header.frame_id = 'map'
  pose.header.stamp = navigator.get_clock().now().to_msg()
  pose.pose.position.x = position_x
  pose.pose.position.y = position_y
  pose.pose.position.z = 0.0
  pose.pose.orientation.x = q_x
  pose.pose.orientation.y = q_y
  pose.pose.orientation.z = q_z
  pose.pose.orientation.w = q_w
  return pose

def main():
  rclpy.init()
  nav = BasicNavigator()

  initial_pose = create_pose_stamped(nav, 0.0, 0.0, 1.57)
  nav.setInitialPose(initial_pose) # -- set the initial_pose always 0,0,0

  nav.waitUntilNav2Active()

  goal_pose1 = create_pose_stamped(nav, 3.5, -5.0, 1.57)
  goal_pose2 = create_pose_stamped(nav, 7.0, -7.5, 0.0)
  goal_pose3 = create_pose_stamped(nav, -2.5, 5.0, 3.14)
  goal_pose4 = create_pose_stamped(nav, -6.5, -3.0, -1.57)
  goal_pose5 = create_pose_stamped(nav, 0.0, 0.0, 1.57)
  
  # -- to go one pose
  #nav.goToPose(goal_pose)
  # while not nav.isTaskComplete():
  #   feedback = nav.feedback()

  # -- follow waypoints
  waypoints = [goal_pose1, goal_pose2, goal_pose3, goal_pose4, goal_pose5]
  nav.followWaypoints(waypoints)
  while not nav.isTaskComplete():
    feedback = nav.getFeedback() 

  print(nav.getResult())

  rclpy.shutdown()

if __name__ == '__main__':
  main()

