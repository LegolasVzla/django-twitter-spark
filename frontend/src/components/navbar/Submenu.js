import React from 'react'
import { NavLink } from 'react-router-dom';
import './Navbar.css';

function Submenu(props) {
    const items = props.subMenuItems;

    const subMenuItems = items.map((item,index) =>
        <li key={item.keyIndex} style={{ listStyleType: 'none'}}>
            <NavLink activeStyle={{ color: 'cyan' }} to={item.path}>
                {/* Warning: findDOMNode is deprecated in StrictMode
                https://github.com/react-bootstrap/react-bootstrap/issues/5075 */}
                {item.icon}
                <span style={{marginLeft: '10px'}}>{item.title}</span>
                {item.badge != null ? (
                    item.badge
                ):null
                }                
            </NavLink>
        </li>
    );

    return (
        <ul>
            {subMenuItems}
        </ul>
    )
}

export default Submenu
