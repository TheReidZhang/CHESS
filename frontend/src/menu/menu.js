import React, { useState } from 'react';
import {useHistory} from 'react-router-dom';
import Modal from 'react-modal';
import './menu.css';
import Button from 'react-bootstrap/Button';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import 'bootstrap/dist/css/bootstrap.min.css';
import ModalBtn from './ModalBtn';


Modal.setAppElement("#root");
function Menu() {
    const [modalIsOpen, setModalIsOpen] = useState(false);
    const [resumeList, setResumeList] = useState([]);

    const history = useHistory();

    const new_game = async() => {
        const response = await fetch('/chess/new', {
            method: 'POST',
            body: JSON.stringify({ 
              mode: "123"})
          });
        const json = await response.json();
        const session = json["session_id"];
        const ret = '/chess/' + session;
        history.push(ret);
    }

    const game_list = async() => {
        const response = await fetch('/resume')
        const json = await response.json();
        const lst = json["resume_list"];
        var ret = []
        for (var i = 0; i < lst.length; i++) {
            ret.push(<ModalBtn key={lst[i]["session_id"]}  session_id={lst[i]["session_id"]} start_time={lst[i]["start_time"]} last_update={lst[i]["last_update"]}/>);
        }
        setResumeList(ret);
    }
    
    return (
        <div className="center-container">
            <Row className="text-center">
                <Col md={12} xs={12} lg={12} sm={12} className="mb-5">
                    <Button variant="outline-dark" size="lg" onClick={new_game} className="myBtn">
                        New Game
                    </Button>
                </Col>

                <Col md={12} xs={12} lg={12} sm={12} className="mb-5">
                    <Button variant="outline-dark" size="lg" className="myBtn" onClick={() => {game_list(); setModalIsOpen(true)}}>
                        Resume Game
                    </Button>
                    <Modal 
                        isOpen={modalIsOpen} 
                        onRequestClose={() => setModalIsOpen(false)}
                        style={
                            {
                                overlay: {
                                    backgroundColor: 'grey'
                                },
                                content: {
                                    backgroundColor: 'orange'
                                }
                            }
                        }>
                        {resumeList}
                    </Modal>
                </Col>
                
                <Col md={12} xs={12} lg={12} sm={12} className="mb-5">
                    <Button variant="outline-dark" className="myBtn" size="lg" onClick={new_game}>
                        Replays
                    </Button>
               </Col>
            </Row>
        </div>
      );
    
  }

export default Menu;
  