import React, { useState } from 'react';
import { Dropdown } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';



function GameOption(props) {
    const [show, setShow] = useState(true)
    const onToggle = (isOpen, e, metadata) => {
        if (metadata["source"] === 'click')
            setShow(!show)
    }

    return (
        <Dropdown show={show} drop="left" onToggle={onToggle}>
        <Dropdown.Toggle variant="outline-light" id="InGameMenu" size="sm">
            MENU
        </Dropdown.Toggle>
        <Dropdown.Menu style={{minWidth: "auto"}}>
            <Dropdown.Item onClick={props.takeback}> 
                <div style={{textAlign: "center", fontSize: "75%"}}>
                    Takeback
                </div>
            </Dropdown.Item>
            <Dropdown.Item > 
                <div style={{textAlign: "center", fontSize: "75%"}}>
                    Resign
                </div>
            </Dropdown.Item>
            <Dropdown.Item > 
                <div style={{textAlign: "center", fontSize: "75%"}}>
                    Draw
                </div>
            </Dropdown.Item>

        </Dropdown.Menu>
    </Dropdown>

    );
}

export default GameOption;