import React from 'react'
import { NavLink } from 'react-router-dom';
import './Navbar.css';

function Submenu(props) {
    const items = props.subMenuItems;

    const subMenuItems = items.map((item,index) =>
        <li key={index.toString()} style={{ listStyleType: 'none'}}>
            <NavLink exact={item.exactPath} activeStyle={{ color: 'cyan' }} to={item.path}>
                {/* https://github.com/react-bootstrap/react-bootstrap/issues/5075 */}
                {item.icon}
                <span>{item.title}</span>
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
