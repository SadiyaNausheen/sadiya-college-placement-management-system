CREATE DATABASE IF NOT EXISTS sadiya_placement_db;
USE sadiya_placement_db;

CREATE TABLE IF NOT EXISTS students (
    student_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    department VARCHAR(50),
    cgpa DECIMAL(3,2)
);

CREATE TABLE IF NOT EXISTS companies (
    company_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL,
    location VARCHAR(100),
    job_role VARCHAR(100),
    package_lpa DECIMAL(5,2),
    eligibility_cgpa DECIMAL(3,2)
);

CREATE TABLE IF NOT EXISTS applications (
    application_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    company_id INT NOT NULL,
    application_date DATE,
    status VARCHAR(30) DEFAULT 'Applied',
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);
