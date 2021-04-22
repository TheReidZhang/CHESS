import React from 'react';
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import Modal from 'react-bootstrap/Modal'
import 'bootstrap/dist/css/bootstrap.min.css';
import {useHistory} from 'react-router-dom';


function Signup(props) {
    const usernameRef = React.createRef();
    const passwordRef = React.createRef();
    const history = useHistory();

    const onFormSubmit = async e => {
        e.preventDefault()
        let user = usernameRef.current.value;
        let pwd = passwordRef.current.value;

        const response = await fetch('/signup', {
            method: 'POST',
            body: JSON.stringify({
            username: user,
            password: pwd})
        });
        const json = await response.json();
        if (json["valid"]) {
            history.go(0);
        }
        else {
            alert("Username already exists!");
            usernameRef.current.value = ""
            passwordRef.current.value = ""
        }
    }

    return (
        <Modal show={props.showSignup} onHide={props.handleSignupClose}>
            <Modal.Header closeButton>
                <Modal.Title>Sign Up</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form onSubmit={onFormSubmit}>
                    <Form.Group controlId="formBasicEmail">
                        <Form.Label>Username</Form.Label>
                        <Form.Control ref={usernameRef} type="Username" placeholder="Enter Username" />
                        <Form.Text className="text-muted">
                            We'll never share your email with anyone else.
                        </Form.Text>
                    </Form.Group>

                    <Form.Group controlId="formBasicPassword">
                        <Form.Label>Password</Form.Label>
                        <Form.Control ref={passwordRef} type="password" placeholder="Password" />
                    </Form.Group>
                    <Button variant="primary" type="submit" className="mt-3 mb-3" style={{width: "100%", backgroundColor: "black"}}>
                        Submit
                    </Button>
                </Form>
            </Modal.Body>
        </Modal>
    );
}

export default Signup;