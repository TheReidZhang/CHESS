import React, { useState } from 'react';
import {useHistory} from 'react-router-dom';
import './menu.css';
import Button from 'react-bootstrap/Button';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import 'bootstrap/dist/css/bootstrap.min.css';
import ModalBtn from './ModalBtn';
import ModalBtn2 from './ModalBtn2';
import Modal from 'react-bootstrap/Modal'

function MainMenu() {
    const [showMode, setShowMode] = useState(false);
    const [resumeIsOpen, setResumeIsOpen] = useState(false);
    const [replayIsOpen, setReplayIsOpen] = useState(false);
    const [resumeList, setResumeList] = useState([]);
    const [replayList, setReplayList] = useState([]);

    const history = useHistory();

    const new_game = async(mode) => {
        const response = await fetch('/chess/new', {
            method: 'POST',
            body: JSON.stringify({ 
              mode: mode})
          });
        const json = await response.json();
        const session = json["session_id"];
        const ret = '/chess/' + session;
        history.push(ret);
    }

    const resume_game = async() => {
        const response = await fetch('/resume')
        const json = await response.json();
        const lst = json["resume_list"];
        var ret = []
        for (var i = 0; i < lst.length; i++) {
            ret.push(<ModalBtn key={lst[i]["session_id"]}  session_id={lst[i]["session_id"]} start_time={lst[i]["start_time"]} last_update={lst[i]["last_update"]} mode={lst[i]["mode"]}/>);
        }
        setResumeList(ret);
        setResumeIsOpen(true);
    }

    const replay_game = async() => {
        const response = await fetch('/replays')
        const json = await response.json();
        const lst = json["replay_list"];
        var ret = []
        for (var i = 0; i < lst.length; i++) {
            ret.push(<ModalBtn2 key={lst[i]["session_id"]}  session_id={lst[i]["session_id"]} start_time={lst[i]["start_time"]} last_update={lst[i]["last_update"]} mode={lst[i]["mode"]}/>);
        }
        setReplayList(ret);
        setReplayIsOpen(true);
    }
    
    return (
        <div className="center-container">
            <Row className="text-center">
                <Col md={12} xs={12} lg={12} sm={12} className="mb-5">
                    <Button variant="outline-dark" size="lg" onClick={() => setShowMode(true)} className="myBtn">
                        New Game
                    </Button>
                    <Modal show={showMode} onHide={() => setShowMode(false)}>
                        <Modal.Header closeButton>
                            <Modal.Title>Choose Mode</Modal.Title>
                        </Modal.Header>
                        <Modal.Body> 
                            <Row className="align-items-center mb-3">
                                <Col>
                                    <div style={{ display: "flex", justifyContent: "center" }}>
                                        <Button variant="outline-dark" size="md" onClick={() => new_game("easy")}>
                                            Easy
                                        </Button>
                                    </div>
                                </Col>
                            </Row>

                            <Row className="align-items-center mb-3">
                                <Col>
                                    <div style={{ display: "flex", justifyContent: "center" }}>
                                        <Button variant="outline-dark" size="md" onClick={() => new_game("pvp")}>
                                            PvP
                                        </Button>
                                    </div>
                                </Col>
                            </Row>
                        </Modal.Body>
                    </Modal>
                </Col>

                <Col md={12} xs={12} lg={12} sm={12} className="mb-5">
                    <Button variant="outline-dark" size="lg" className="myBtn" onClick={resume_game}>
                        Resume Game
                    </Button>
                    <Modal show={resumeIsOpen} onHide={() => setResumeIsOpen(false)}>
                        <Modal.Header closeButton>
                            <Modal.Title>Resume</Modal.Title>
                        </Modal.Header>
                        <Modal.Body> 
                            {resumeList}
                        </Modal.Body>
                    </Modal>
                </Col>
                
                <Col md={12} xs={12} lg={12} sm={12} className="mb-5">
                    <Button variant="outline-dark" className="myBtn" size="lg" onClick={replay_game}>
                        Replays
                    </Button>
                    <Modal show={replayIsOpen} onHide={() => setReplayIsOpen(false)}>
                        <Modal.Header closeButton>
                            <Modal.Title>Replays</Modal.Title>
                        </Modal.Header>
                        <Modal.Body> 
                            {replayList}
                        </Modal.Body>
                    </Modal>
               </Col>
            </Row>
        </div>
      );
    
  }

export default MainMenu;
  