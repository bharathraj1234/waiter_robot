# 🤖 ROS2 Waiter Robot (FSM-Based Autonomous Delivery)

## 📌 Overview

This project implements an autonomous waiter robot using ROS2 that performs food delivery tasks inside a restaurant environment. The robot follows a Finite State Machine (FSM) to handle order processing, navigation, confirmation, cancellation, and timeout scenarios.

The system is designed to simulate a real-world restaurant workflow where the robot collects food from the kitchen and delivers it to multiple tables efficiently.

---

## 🧠 System Architecture

* **FSM Node (`main.py`)** → Decision making and state transitions
* **Navigator (`navigator.py`)** → Handles robot movement using Nav2
* **ROS Topics:**

  * `/order` → Receive table orders
  * `/confirm` → Confirmation from kitchen/table
  * `/cancel` → Cancel ongoing task

---

## 🔄 FSM Design

The robot operates using the following states:

* `IDLE` → Waiting for orders
* `WAIT_KITCHEN` → Waiting for kitchen confirmation
* `NEXT_TABLE` → Selecting next table
* `WAIT_TABLE` → Waiting for delivery confirmation
* `RETURN_KITCHEN` → Returning leftover food
* `RETURN_HOME` → Returning to home position

---

## ⚙️ Features Implemented

✅ Single and multiple order handling
✅ Queue-based delivery system
✅ Timeout handling (kitchen & table)
✅ Cancel handling during navigation
✅ Skip unresponsive tables
✅ Conditional return to kitchen
✅ Integration with Nav2 and Gazebo

---

## 🎯 Scenarios Covered

1. Single order delivery
2. Timeout without confirmation
3. Kitchen confirmed but table unresponsive → return to kitchen → home
4. Cancel during movement
5. Multiple order delivery
6. Skip unresponsive tables and continue
7. Skip cancelled table and continue delivery

---

## 🚀 How to Run

### Terminal 1 (Launch simulation)

```bash
ros2 launch waiter_robot custom_world.launch.py
```

### Terminal 2 (Run FSM node)

```bash
ros2 run waiter_robot main
```

### Terminal 3 (Control robot)

#### Send Order

```bash
ros2 topic pub /order std_msgs/String "data: 'table1'" --once
```

#### Confirm (Kitchen/Table)

```bash
ros2 topic pub /confirm std_msgs/String "data: 'yes'" --once
```

#### Reject (Kitchen)

```bash
ros2 topic pub /confirm std_msgs/String "data: 'no'" --once
```

#### Cancel Task

```bash
ros2 topic pub /cancel std_msgs/String "data: 'cancel'" --once
```

---

## 🧪 Example Workflow

1. Robot starts at home
2. Receives order → moves to kitchen
3. Waits for confirmation
4. Collects food → delivers to tables sequentially
5. Handles skip/cancel scenarios
6. Returns to home or kitchen based on conditions

---

## 📌 Design Approach

The system is implemented using a **Finite State Machine (FSM)** where each state represents a stage of operation. Transitions are triggered by:

* Topic messages (`/order`, `/confirm`, `/cancel`)
* Timeout conditions
* Internal flags (food collected, skipped tables)

This approach ensures modularity, clarity, and scalability.

---

## 🚀 Future Improvements

* Non-blocking navigation (asynchronous FSM)
* GUI interface for user interaction
* Priority-based order handling
* Multi-robot coordination

---

## 👨‍💻 Author

**Bharath Raj**
Robotics & Automation Engineering
Passionate about ROS, autonomous systems, and real-world robotics applications
