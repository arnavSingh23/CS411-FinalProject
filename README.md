# Student Grade Tracker

## **Overview**
The **Student Grade Tracker** is a web application designed to help students track their grades, visualize performance trends, and receive reminders for improving attendance in classes where their grades are low. The application integrates with external APIs to fetch relevant resources and schedule data, ensuring a personalized and effective experience.

---

## **Features**

### **1. Grade Management**
- Log grades for different subjects or assignments.
- Calculate average grades automatically based on predefined class grading strategies.
- Visualize grade trends over time using graphical representations.

### **2. Attendance Warnings**
- Fetch class schedules from Google Calendar.
- Identify low-grade courses and warn students to attend their classes.

### **3. Resource Recommendations**
- Fetch study resources (e.g., video tutorials) from external APIs like YouTube.
- Provide personalized recommendations for improving grades in specific subjects.

### **4. Account Management**
- Securely store user credentials (hashed and salted passwords).
- Enable user registration, login, and password updates.

### **5. Health Check**
- Verify that the application is running through a dedicated health-check route.

---

## **Routes**

### **Authentication Routes**
- **`/login`**:
  - **Request Type**: POST
  - **Purpose**: Verify user credentials.
  - **Request Format**: JSON body containing `username` and `password`.
  - **Response Format**: JSON indicating success or failure.

- **`/create-account`**:
  - **Request Type**: POST
  - **Purpose**: Allow users to register.
  - **Request Format**: JSON body containing `username` and `password`.
  - **Response Format**: JSON indicating success or failure.

- **`/update-password`**:
  - **Request Type**: PUT
  - **Purpose**: Enable users to update their password.
  - **Request Format**: JSON body containing `username`, `old_password`, and `new_password`.
  - **Response Format**: JSON indicating success or failure.

### **Grade Management Routes**
- **`/grades/log`**:
  - **Request Type**: POST
  - **Purpose**: Log grades for a specific class or assignment.
  - **Request Format**: JSON body with class name, assignment type, and grade.
  - **Response Format**: JSON confirming grade entry.

- **`/grades/average`**:
  - **Request Type**: GET
  - **Purpose**: Calculate and retrieve average grades for a specific class.
  - **Request Format**: Query parameter for class name.
  - **Response Format**: JSON with the calculated average.

- **`/grades/trends`**:
  - **Request Type**: GET
  - **Purpose**: Visualize grade trends over time.
  - **Response Format**: JSON containing data points for grade visualization.

### **Attendance and Warning Routes**
- **`/calendar/events`**:
  - **Request Type**: GET
  - **Purpose**: Fetch upcoming class events from Google Calendar.
  - **Response Format**: JSON containing event details (e.g., class name, date, time).

- **`/grades/warnings`**:
  - **Request Type**: GET
  - **Purpose**: Generate warnings for classes with low grades.
  - **Response Format**: JSON listing warnings with class details and event times.

### **Resource Recommendation Routes**
- **`/resources/recommend`**:
  - **Request Type**: GET
  - **Purpose**: Fetch educational resources from YouTube or other external APIs.
  - **Response Format**: JSON with recommended resources (e.g., titles, URLs).

### **Health Check Route**
- **`/health-check`**:
  - **Request Type**: GET
  - **Purpose**: Verify the app is running.
  - **Response Format**: JSON confirming app health.

---

## **Setup and Installation**

### **1. Prerequisites**
- Python 3.9+
- Flask
- SQLite
- Docker (optional for containerization)

### **2. Installation Steps**
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/student-grade-tracker.git
   ```
2. Navigate to the project directory:
   ```bash
   cd student-grade-tracker
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up the `.env` file:
   - Add your Google API credentials and other environment variables.
   - Example:
     ```env
     GOOGLE_API_KEY=your_google_api_key
     CLIENT_SECRET_FILE=path_to_your_client_secret.json
     ```
5. Run the application:
   ```bash
   python app.py
   ```

### **3. Docker Setup (Optional)**
- Build and run the Docker container:
  ```bash
  docker build -t student-grade-tracker .
  docker run -p 5000:5000 student-grade-tracker
  ```

---

## **Testing**

### **1. Unit Tests**
- Run unit tests to ensure functionality:
  ```bash
  pytest tests/
  ```

### **2. Smoke Test**
- Verify the app launches and performs basic functions without errors.

---

## **API Keys and Environment Variables**
- Use a `.env` file to manage API keys and sensitive data.
- Ensure no secrets are exposed in the GitHub repository.

---

## **Future Enhancements**
- Add support for custom grading strategies by teachers.
- Allow students to manually input attendance data.
- Integrate advanced data visualization for performance trends.

---

## **License**
This project is licensed under the MIT License. See the LICENSE file for details.
