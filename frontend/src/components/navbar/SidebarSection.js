import React, {useState} from 'react'
import * as FaIcons from "react-icons/fa";
import { NavLink } from 'react-router-dom';
import './Navbar.css';
import { Accordion,Button } from 'react-bootstrap'
import Submenu from './Submenu'

function SidebarSection(props) {
    const sidebarItems = props.sidebarItems;
    const customActiveStyle = {
        color: 'cyan'
    };
    const [submenu,setSubmenu] = useState(false);
    const showSubmenu = () => setSubmenu(!submenu);

    return (
        <div className='nav-menu-subsection'>
            {/* Section title */}
            <h3 className='nav-menu-titles'>
                {sidebarItems.title}
            </h3>
            {/* Section items */}
            {sidebarItems.section.map((item,index) => {
                return (
                    <li key={index} className={item.cName} >
                        {/* If the current item has a submenu, display fa caret down icon for each sub item */}
                        {item.dropDownList.length > 0 ? (
                            <Accordion style={{ width: '245px'}}>
                                <Accordion.Toggle bsPrefix='nav-menu-accordion' as={Button} eventKey="0">
                                    <NavLink exact={item.exactPath} activeStyle={customActiveStyle} to={item.path} onClick={showSubmenu}>
                                        {item.icon}
                                        <span>{item.title}</span>
                                        {submenu ? <FaIcons.FaCaretDown/> : <FaIcons.FaCaretRight/>}
                                    </NavLink>
                                </Accordion.Toggle>
                                <Accordion.Collapse eventKey="0">
                                    <Submenu subMenuItems = {item.dropDownList} />
                                </Accordion.Collapse>
                            </Accordion>
                        ) : (
                            <NavLink exact={item.exactPath} activeStyle={customActiveStyle} to={item.path}>
                                {item.icon}
                                <span>{item.title}</span>
                            </NavLink>
                        )}
                    </li>
                )
            })}
        </div>
    )
}

export default SidebarSection
