import Navigation from './navbar'
import Login from './login'
import Signup from './signup'
import React, { useState } from 'react';

function Page(props) {
    const [showLogin, setShowLogin] = useState(false);
    const handleLoginClose = () => setShowLogin(false);
    const handleLoginShow = () => setShowLogin(true);

    const [showSignup, setShowSignup] = useState(false);
    const handleSignupClose = () => setShowSignup(false);
    const handleSignupShow = () => setShowSignup(true);

    return (
        <div>
            <Navigation handleLoginShow={handleLoginShow} isLoggedIn={false}/>
            <Login showLogin={showLogin} handleLoginClose={handleLoginClose} handleSignupShow={handleSignupShow}/>
            <Signup showSignup={showSignup} handleSignupClose={handleSignupClose} />
            <h1>Hello, {props.name}</h1>
        </div>
    );
}

export default Page;