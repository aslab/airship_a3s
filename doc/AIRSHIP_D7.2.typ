#set heading(numbering: "1.")

#title[D7.2 Report on UWV metacontroller for self-awareness]

= Executive summary
//TODO: Update section to include T7.3 items context too.
This report provides an overview of Task 7.2 and 7.3 from the Work Package (WP) 7 of the AIRSHIP project. Focusing on the research and strategies chosen for the development of self-awareness, anticipation and adaptation system for autonomous Wing-In-Ground (WIG) drone operation.

WP 7 is centered around the mission avionics for the Unmanned WIG Vehicle (UWV). This covers guidance and navigation, as well as situational and self-awareness for the efficient and safe mission completion.

// Maybe Task 5.1 WIG System modelling could be also be mentioned in case the metacontroller evaluetes or makes something like considering lift-ratio. Look at T 5.4 implementation as they did use something like that. 
This deliverable focuses on Task 7.2 describing the research and development accomplished with the system self-awareness. This system builds upon the design and systems carried out in Task 3.4 AIRSHIP-1 Design (WP 3), Task 5.3 Software-in-the-loop (SITL) and Hardware-in-the-loop (HITL), Task 5.4 Supervisory operator interfaces (WP 5), Task 6.4 Situational awareness (WP 6) and Task 8.1 Integration and construction (WP 8). Whose systems provide the self-awareness with the mechanisms to read the current state of its internal components and external surroundings and adapt in accordance to the mission requirements.

// TODO: Did this task complete its objectives?

= Introduction
This project is conceived within the context of vehicle transport over the waters of the many European archipelagos. Here we propose the UWV as the solution for a more efficient than airplanes but faster than boats alternative vehicle.

For this drone to work in open-ended environments autonomously we propose a metacontroller system for handling the drone in adverse situations and achieve the mission. All of this while considering the constraints, values and goals imposed by the stakeholders and designers.

We build upon the SysSelf metacontroller to achieve the objectives required. By developing a metamodel that represents the aircraft capabilities, components, values and goals within the environment and mission that the system will work on.

The metacontroller is implemented in the Companion Computer, as another module of the Flight Management System (FMS), and carries out its purpose by interacting with the aircraft through the middleware Robot Operating System (ROS).

Validation and testing of the metacontroller capabilities will be carried out through the execution of simulated case scenarios.

== Purpose of the Deliverable
The purpose of this deliverable is to document the research and development process of the self-awareness system. Including the integration with the UWV components from other WP. The following activities has been conducted during Task 7.2.
+ State of the art research in the literature on self-adapting/self-awareness methods for robotic applications.  // The papers we read, implementations we studied etc.
// TODO: discuss the relevance of this point, as it is not precisely mentioned in the DoA. Also, check if the other deliverables contain some similar section.
+ Analysis on structure, components and software capabilities of the aircraft for later usage by the metacontroller.  // How many sensors there are, how are they configured, can they be reconfigured, is there redundancy...
+ Development of the software environment and tools.  // Container image creation, building scripts, ROS package, simulation setup...
+ Development of the metamodel and metacontroller.  // OWL codification of the aircraft capabilities, components, goals. ROS node implementation of the metacontroller...
+ Simulated testing of the metacontroller.  // Simulated scenarios conducted.

== Document structure
//TODO

= State of the art on Self-Adapting robotics
//TODO Mention papers, Esther work, implementations and why did we choose sysself.

= AIRSHIP System Structure and Metamodel
The AIRSHIP-1 operating in the archipelagos seas for cargo delivery are the vehicle, environment and mission considered when modeling the system.

== Hardware components
=== Flight Control Systems (FCS)
The system will have 2 Pixhawks 6A. Each FCS will work as the embedded system for handling the actuators and proppelers. Two complete FCS will be installed in the aircraft to have a fallback should one of them give trouble. These FCS also include many sensors (IMU, magnetometer, barometer) to provide a localization system although they are not used as primary source. Software-side, they run Ardupilot firmware.

=== Companion Computer (CC)
This is the computer hardware that will link the many sensors used in the Localization (T6.1) @airship_d61 and Situational Awareness (T6.4) Systems with the FCS. The software stack used to do so is ROS 2 for handling the sensors and message distribution. Ardupilot for the autopilot and actuator functionality and MAVROS to link the ROS middleware with the Ardupilot stack and the Ground Control Station (GCS).

=== Localization Sensors
+ IMU
+ GNSS
+ 2 Altimeters
+ Magnetometer
+ Pitot

=== Situational awareness sensors
+ LIDAR
+ RADAR
+ IR Camera
+ EO Camera

= Software suite
//TODO

= Case scenarios
== Scenario 1: Communication loss
+ Drone is flying towards mission objective.
+ Communication with GCS is lost.
+ Reconnection timeout exceeds safety limits. The Safety value decreases.
+ The metacontroller revaluates possible alternative capabilities or components categories to keep up with the safety value. But finds only as viable solution the change in mission goal. 
+ A return to last established connection within traveled Waypoints is reconfigured as alternative mission goal.
+ Once the drone reconnects with GCS it either lands or loiters in position to inform the operator and await further instructions.

== Scenario 2: Battery drainage
+ Drone flies towards mission objective.
+ Battery monitor estimates insufficient energy to reach the target. 
+ Metacontroller considers alternative solutions but finds only Mission goal change as viable.
+ Mission goal is set to Either Return To Launch (RTL) if viable or land at a near safe location and inform Supervisory System.

== Scenario 3: Localization System failure
+ During drone flight.
+ Sensor monitor considers main Localization System unavailable.
+ A reconfiguration request is triggered. The metacontroller searches for alternative components.
+ Metacontroller finds as alternative solution the redundant Flight Control System sensors for localization.
+ Mission continues with alternative sensors. Informing about the changes. //Communicating also safety, efficiency value changes too?

= Glossary
\ CC: Companion Computer
\ FCS: Flight Control System
\ FMS: Flight Management System
\ GCS: Ground Control System
\ HITL: Hardware-in-the-loop
\ KR&R: Knowledge Representation and Reasoning
\ ROS: Robot Operating System
\ RTL: Return To Launch
\ SITL: Software-in-the-loop
\ UWV: Unmanned WIG Vehicle
\ WIG: Wing-in-ground
\ WP: Work Package

#bibliography("AIRSHIP_D7.2_bibliography.yaml")
