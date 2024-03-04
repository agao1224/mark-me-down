import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Button, Form, Container, Row, Col } from 'react-bootstrap';

function App() {
  const [courses, setCourses] = useState([]);

  useEffect(() => {
    fetch('http://localhost:8000/courses/')
      .then(response => response.json())
      .then(data => setCourses(data))
      .catch(error => console.error('Error fetching courses:', error));
  }, []);

  const handleSubmit = (courseTitle, formLink, e) => {
    e.preventDefault();
    const data = {
      course_title: courseTitle,
      form_link: formLink,
    };

    fetch('http://localhost:8000/courses/update_link', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
      // Optionally refresh the courses list or show feedback
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  };

  const handleAddCourse = (e) => {
    e.preventDefault();
    const title = e.target.elements.title.value;
    const courseRegex = /^\d{2}-\d{3}$/;

    if (!courseRegex.test(title)) {
      alert('Error: The course title is poorly formatted. Please use the format XX-XXX.');
      return;
    }

    fetch('http://localhost:8000/courses/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        "title": title,
      })
    })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
      setCourses([...courses, data]);
    })
    .catch(error => {
      console.error('Error:', error);
    });
  };

  return (
    <Container>
      <br />
      <h1>Courses</h1>
      <h5>Once attendance link for course is updated, emails are broadcast to all subscribers. Please be kind &#60;3 </h5>
      <br /><br /><br />
      {courses.map(course => (
        <Row key={course.title} className="mb-3">
          <Col>
            <div>{course.title}</div>
          </Col>
          <Col>
            <Form onSubmit={(e) => handleSubmit(course.title, e.target.elements.formLink.value, e)}>
              <Form.Group controlId="formLink">
                <Form.Control type="text" placeholder="attendance link" name="formLink" />
              </Form.Group>
              <Button variant="primary" type="submit">
                Update Attendance Link
              </Button>
            </Form>
          </Col>
        </Row>
      ))}
      <Row className="mb-3">
        <Col>
          <Form onSubmit={handleAddCourse}>
            <Form.Group controlId="title">
              <Form.Control type="text" placeholder="Enter course title (XX-XXX)" name="title" />
            </Form.Group>
            <Button variant="primary" type="submit">
              Add Another Course
            </Button>
          </Form>
        </Col>
      </Row>
    </Container>
  );
}

export default App;
