import React,{useState} from 'react'
import * as FaIcons from "react-icons/fa";
import * as AiIcons from "react-icons/ai";
import { Link } from 'react-router-dom';
import { TopSidebarData, BottomSidebarData } from './SidebarData';
import './Navbar.css';
import { IconContext } from 'react-icons'
import SidebarSection from './SidebarSection'
import { Navbar, NavDropdown, Nav } from 'react-bootstrap'
// import Dropdown from './Dropdown'

function CustomNavbar() {
    const [sidebar,setSidebar] = useState(false);
    const showSidebar = () => setSidebar(!sidebar);

    const sidebarItems = [
        {
            title: 'General',
            section: TopSidebarData
        },
        {
            title: 'Estadísticas',
            section: BottomSidebarData
        }
    ];
    
    return (
        <>
            <IconContext.Provider value={{ color: '#fff'}}>
                <Navbar collapseOnSelect expand="lg" variant="dark">
                <Navbar.Brand href="/" style={{ color: '#fff'}}>
                    <AiIcons.AiOutlineFileSearch style={{ fontSize: '2rem' }}/> Topic Analyzer
                </Navbar.Brand>
                <Navbar.Toggle aria-controls="responsive-navbar-nav" />
                <Navbar.Collapse id="responsive-navbar-nav">
                    <Nav className="mr-auto">
                        <Nav.Link href="#" className='menu-bars'>
                            <FaIcons.FaBars onClick={showSidebar} />
                        </Nav.Link>
                    </Nav>
                    <Nav>
                        <Nav className="navbar">
                            <NavDropdown title="Usuario" id="collasible-nav-dropdown">
                                <NavDropdown.Item href="/profile">Ver Mi Perfil</NavDropdown.Item>
                                <NavDropdown.Divider />
                                <NavDropdown.Item href="/">Cerrar Sesión</NavDropdown.Item>
                            </NavDropdown>
                            <Nav.Link></Nav.Link>
                        </Nav>
                    </Nav>
                </Navbar.Collapse>
                </Navbar>
            </IconContext.Provider>
            {/* Sidebar Section */}
            <nav className={sidebar ? 'nav-menu active' : 'nav-menu'}>
                <ul className='nav-menu-items'>
                    <Link to='#' className='close-icon-menu-bars' onClick={showSidebar}>
                        <AiIcons.AiOutlineClose style={{ marginTop: '1.2rem'}} />
                    </Link>
                    <SidebarSection sidebarItems={sidebarItems[0]} />
                    <SidebarSection sidebarItems={sidebarItems[1]} />
                </ul>
            </nav>
        </>
    )
}

export default CustomNavbar
