cmake_minimum_required(VERSION 3.5)
project(r2m_4wd_diff_description)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY r2m_4wd_diff_description/urdf r2m_4wd_diff_description/rviz
  DESTINATION share/${PROJECT_NAME}/r2m_4wd_diff_description
)

ament_package()
