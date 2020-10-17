import React,{useState} from 'react'
import * as FaIcons from "react-icons/fa";
import * as AiIcons from "react-icons/ai";
import { Link } from 'react-router-dom';
import { TopSidebarData, BottomSidebarData } from './SidebarData';
import './Navbar.css';
import { IconContext } from 'react-icons'
import SidebarSection from './SidebarSection'

function Navbar() {
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
    ]    
    
    return (
        <>
            <IconContext.Provider value={{ color: '#fff'}}>
                {/* Navbar section */}
                <div className="navbar">
                    <div className="mb-2 navbar-title">
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
                        <SidebarSection sidebarItems={sidebarItems[0]} />
                        <SidebarSection sidebarItems={sidebarItems[1]} />
                    </ul>
                </nav>
            </IconContext.Provider>
        </>
    )
}

export default Navbar
