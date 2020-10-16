import React,{useState} from 'react'
import * as FaIcons from "react-icons/fa";
import * as AiIcons from "react-icons/ai";
import { Link, NavLink } from 'react-router-dom';
import { TopSidebarData, BottomSidebarData } from './SidebarData';
import './Navbar.css';
import { IconContext } from 'react-icons'
import Accordion from 'react-bootstrap/Accordion'
import Button from 'react-bootstrap/Button'
import Submenu from './Submenu'

function Navbar() {
    const [sidebar,setSidebar] = useState(false);

    // const onMouseEnter = () => {
    //     if(window.innerWidth < 960) {
    //         setSidebar(false);
    //     }else{
    //         setSidebar(true);
    //     }
    // };

    // const onMouseLeave = () => {
    //     if(window.innerWidth < 960) {
    //         setSidebar(false);
    //     }else{
    //         setSidebar(false);
    //     }
    // }

    const showSidebar = () => setSidebar(!sidebar)
    
    return (
        <>
            <IconContext.Provider value={{ color: '#fff'}}>
                {/* Navbar section */}
                <div className="navbar">
                    <div style={{ width: '10rem', fontSize: 'large', marginTop: '5px' }} className="mb-2">
                            <p style={{ color: '#fff'}}>
                                <AiIcons.AiOutlineFileSearch style={{ fontSize: '2rem'  }}/> Topic Analyzer
                            </p>
                    </div>
                    <Link to="#" className='menu-bars'>
                        {/* Burger icon */}
                        <FaIcons.FaBars onClick={showSidebar} />
                    </Link>
                </div>
                {/* Sidebar section */}
                <nav className={sidebar ? 'nav-menu active' : 'nav-menu'}>
                    <ul className='nav-menu-items'>
                        <Link to='#' className='close-icon-menu-bars' onClick={showSidebar}>
                            {/* X's icon */}
                            <AiIcons.AiOutlineClose style={{ marginTop: '1.2rem'}} />
                        </Link>
                        {/* <li className='navbar-toggle'></li> */}
                        <div className='nav-menu-subsection'>
                            <h3 className='nav-menu-titles' style={{margin: '1rem'}}>General</h3>
                            {TopSidebarData.map((item,index) => {
                                return (
                                    <li key={index} className={item.cName} >
                                        {/* If the current item has a submenu, display fa caret down*/}
                                        {item.dropDownList.length > 0 ? (
                                            <Accordion style={{ width: '245px'}}>
                                                <Accordion.Toggle bsPrefix='nav-menu-accordion' as={Button} style={{ borderStyle: 'hidden' }} eventKey="0">
                                                    <NavLink exact={item.exactPath} activeStyle={{color: 'cyan'}} to={item.path}>
                                                        {item.icon}
                                                        <span>{item.title}</span>
                                                        <FaIcons.FaCaretDown/>
                                                    </NavLink>
                                                </Accordion.Toggle>
                                                <Accordion.Collapse eventKey="0">
                                                    <Submenu subMenuItems = {item.dropDownList} />
                                                </Accordion.Collapse>
                                            </Accordion>
                                        ) : (
                                            <NavLink exact={item.exactPath} activeStyle={{color: 'cyan'}} to={item.path}>
                                                {item.icon}
                                                <span>{item.title}</span>
                                            </NavLink>
                                        )}
                                    </li>
                                )
                            })}
                        </div>
                        <div className='nav-menu-subsection'>
                            <h3 className='nav-menu-titles' style={{margin: '1rem'}}>Estadísticas</h3>                        
                            {BottomSidebarData.map((item,index) => {
                                return (
                                    <li key={index} className={item.cName} >
                                        {/* If the current item has a submenu, display fa caret down*/}
                                        {item.dropDownList.length > 0 ? (
                                            <Accordion style={{ width: '245px'}}>
                                                <Accordion.Toggle bsPrefix='nav-menu-accordion' as={Button} style={{ borderStyle: 'hidden' }} eventKey="0">
                                                    <NavLink exact={item.exactPath} activeStyle={{color: 'cyan'}} to={item.path}>
                                                        {item.icon}
                                                        <span>{item.title}</span>
                                                        <FaIcons.FaCaretDown/>
                                                    </NavLink>
                                                </Accordion.Toggle>
                                                <Accordion.Collapse eventKey="0">
                                                    <Submenu subMenuItems = {item.dropDownList} />
                                                </Accordion.Collapse>
                                            </Accordion>
                                        ) : (
                                            <NavLink exact={item.exactPath} activeStyle={{color: 'cyan'}} to={item.path}>
                                                {item.icon}
                                                <span>{item.title}</span>
                                            </NavLink>
                                        )}
                                    </li>
                                )
                            })}
                        </div>
                    </ul>
                </nav>
            </IconContext.Provider>
        </>
    )
}

export default Navbar
