import React, { useState } from 'react';
import {useHistory} from 'react-router-dom';
import Modal from 'react-modal';
import './menu.css';
import Button from 'react-bootstrap/Button';
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
        <div className="div-center">
            <div className="container">
                <div className="row mt-2 mb-5 text-center">
                    <div className="col-12">
                        Chess Game
                    </div>
                </div>

                <div className="row mb-4 text-center">
                    <div className="col-12">
                        <Button onClick={new_game}>
                            New Game
                        </Button>
                    </div>
                </div>

                <div className="row mb-4 text-center">
                    <div className="col-12">
                        <Button onClick={() => {game_list(); setModalIsOpen(true)}}>
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
                    </div>
                </div>

                <div className="row mb-4 text-center">
                    <div className="col-12">
                        <Button onClick={new_game}>
                            Replays
                        </Button>
                    </div>
                </div>
            </div>
        </div>
      );
    
  }

export default Menu;
  