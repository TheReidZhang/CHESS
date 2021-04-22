import React, { useEffect, useState } from 'react';
import { Card } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';



function Info(props) {

    const [time, setTime] = useState(new Date().toLocaleString());

    useEffect(() => {
        let secTimer = setInterval( () => {
            setTime(new Date().toLocaleString())
        },1000)

        return () => clearInterval(secTimer);
    }, []);

    return (
        <Card bg="light" border="dark"  className="text-center" style={{fontSize:"10px"}}>
                <Card.Header>
                    Game Info
                </Card.Header>
                <Card.Body >
                    <Card.Text >
                        Time: {time} <br/>
                        Mode: {props.mode.toUpperCase()} <br/>
                        Turn: {props.turn} <br/>
                        Status: {props.status}
                    </Card.Text>
                </Card.Body>
        </Card>

    );
}

export default Info;