import React,{useState} from 'react'
import * as FaIcons from "react-icons/fa";
import * as AiIcons from "react-icons/ai";
import { Link } from 'react-router-dom';
import { TopSidebarData, BottomSidebarData } from './SidebarData';
import './Navbar.css';
import { IconContext } from 'react-icons'
import Card from 'react-bootstrap/Card'
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
                    <Card style={{ width: '11rem' }} className="mb-2">
                        <Card.Header>
                            <h3 style={{ color: '#fff', marginLeft: '1rem'}}>
                                <AiIcons.AiOutlineFileSearch style={{ fontSize: '1.5rem'  }}/> Topic Analyzer
                            </h3>
                        </Card.Header>
                    </Card>
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
                            <h3 className='nav-menu-titles'>General</h3>
                            {TopSidebarData.map((item,index) => {
                                return (
                                    <li key={index} className={item.cName} >
                                        {/* If the current item has a submenu, display fa caret down*/}
                                        {item.dropDownList.length > 0 ? (
                                            <Link to={item.path}>
                                                {item.icon}
                                                <span>{item.title}</span>
                                                <FaIcons.FaCaretDown />
                                                <Submenu subMenuItems = {item.dropDownList} />
                                            </Link>
                                        ) : (
                                            <Link to={item.path}>
                                                {item.icon}
                                                <span>{item.title}</span>
                                            </Link>
                                        )}
                                    </li>
                                )
                            })}
                        </div>
                        <div className='nav-menu-subsection'>
                            <h3 className='nav-menu-titles'>Estadísticas</h3>                        
                            {BottomSidebarData.map((item,index) => {
                                return (
                                    <li key={index} className={item.cName} >
                                        {/* If the current item has a submenu, display fa caret down*/}
                                        {item.dropDownList.length > 0 ? (
                                            <Link to={item.path}>
                                                {item.icon}
                                                <span>{item.title}</span>
                                                <FaIcons.FaCaretDown />
                                                <Submenu subMenuItems = {item.dropDownList} />
                                            </Link>
                                        ) : (
                                            <Link to={item.path}>
                                                {item.icon}
                                                <span>{item.title}</span>
                                            </Link>
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
