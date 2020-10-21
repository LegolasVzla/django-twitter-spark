import React from 'react'
import * as FaIcons from "react-icons/fa";
import { Accordion,Button } from 'react-bootstrap'
import { DropdownData } from './DropdownData';
import { NavLink } from 'react-router-dom';

function Dropdown() {

    const subMenuItems = DropdownData.map((item,index) =>
        <li key={index.toString()} style={{ listStyleType: 'none'}}>
            <NavLink exact={item.exactPath} to={item.path}>
                {/* https://github.com/react-bootstrap/react-bootstrap/issues/5075 */}
                {item.icon}
                <span>{item.title}</span>
            </NavLink>
        </li>
    );

    return (
        <div className="dropdown">
            <Accordion style={{ width: '245px'}}>
                <Accordion.Toggle bsPrefix='nav-menu-accordion' as={Button} eventKey="0">
                    <span style={{ color: '#fff'}}>
                        Usuario
                    </span>
                    <FaIcons.FaCaretDown/>
                </Accordion.Toggle>
                <Accordion.Collapse eventKey="0">
                    <ul>
                        {subMenuItems}
                    </ul>
                </Accordion.Collapse>
            </Accordion>
        </div>
    )
}

export default Dropdown
