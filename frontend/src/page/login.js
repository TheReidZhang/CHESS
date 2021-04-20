import React, {useState, useEffect} from 'react';
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import Modal from 'react-bootstrap/Modal'
import 'bootstrap/dist/css/bootstrap.min.css';
import {useHistory} from 'react-router-dom';

function Login(props) {
    const history = useHistory();
    const usernameRef = React.createRef();
    const passwordRef = React.createRef();

    const onFormSubmit = async e => {
        e.preventDefault()
        let user = usernameRef.current.value;
        let pwd = passwordRef.current.value;

        const response = await fetch('/login', {
            method: 'POST',
            body: JSON.stringify({
            username: user,
            password: pwd})
        });
        const json = await response.json();
        if (json["valid"]) {
            history.go(0);
        }
    }

    return (
        <Modal show={props.showLogin} onHide={props.handleLoginClose}>
            <Modal.Header closeButton>
                <Modal.Title>Log In</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form onSubmit={onFormSubmit}>
                    <Form.Group controlId="formBasicUsername">
                        <Form.Label>Username</Form.Label>
                        <Form.Control ref={usernameRef} type="username" placeholder="Enter username" />
                        <Form.Text className="text-muted">
                            We'll never share your information with anyone else.
                        </Form.Text>
                    </Form.Group>

                    <Form.Group controlId="formBasicPassword">
                        <Form.Label>Password</Form.Label>
                        <Form.Control ref={passwordRef} type="password" placeholder="Password" />
                    </Form.Group>
                    <Form.Group controlId="formBasicCheckbox">
                        <Form.Check type="checkbox" label="Remember my password" />
                    </Form.Group>
                    <Button variant="primary" type="submit" className="mb-3" style={{width: "100%", backgroundColor: "black"}}>
                        Submit
                    </Button>
                    <Button variant="light" onClick={() => {props.handleSignupShow(); props.handleLoginClose();}} className="mb-3" style={{width: "100%", borderColor: "black"}}>
                        Become New Member
                    </Button>
                </Form>
            </Modal.Body>
        </Modal>
    );
}

export default Login;