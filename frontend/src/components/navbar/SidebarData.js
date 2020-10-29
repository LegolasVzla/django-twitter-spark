import React from 'react';
import * as AiIcons from "react-icons/ai";
import * as BiIcons from "react-icons/bi";
import * as FaIcons from "react-icons/fa";
import Badge from 'react-bootstrap/Badge'

export const TopSidebarData = [
    {
        title: 'Home',
        path: '/',
        icon: <AiIcons.AiFillHome />,
        cName: 'nav-text',
        dropDownList: [],
        keyIndex: 1
    },
    {
        title: 'Buscar Palabras',
        path: '#',
        icon: <BiIcons.BiSearchAlt />,
        cName: 'nav-text',
        dropDownList: [
            {
                title: 'Twitter',
                path: '/search-twitter',
                icon: <FaIcons.FaGenderless style={{ marginLeft: '1rem'}} />,
                cName: 'nav-text',
                keyIndex: 1.1,
                badge: null
            },
            {
                title: "Facebook",
                path: '/search-fb',
                icon: <FaIcons.FaGenderless style={{ marginLeft: '1rem'}} />,
                cName: 'nav-text',
                keyIndex: 1.2,
                badge: <Badge style={{marginLeft: '1rem'}} variant="success">Soon</Badge>                
            },
            {
                title: "Instagram",
                path: '/search-ig',
                icon: <FaIcons.FaGenderless style={{ marginLeft: '1rem'}} />,
                cName: 'nav-text',
                keyIndex: 1.3,
                badge: <Badge style={{marginLeft: '1rem'}} variant="success">Soon</Badge>                
            }
        ],
        keyIndex: 2
    },
    {
        title: 'Ver mi Diccionario',
        path: '/customdictionary',
        icon: <BiIcons.BiFile />,
        cName: 'nav-text',
        dropDownList: [],
        keyIndex: 3
    }
]

export const BottomSidebarData = [
    {
        title: 'Buscar Recientes',
        path: '#',
        icon: <FaIcons.FaChartBar />,
        cName: 'nav-text',
        dropDownList: [
            {
                title: 'Twitter',
                path: '/recent-twitter',
                icon: <FaIcons.FaGenderless style={{ marginLeft: '1rem'}} />,
                cName: 'nav-text',
                keyIndex: 2.1,
                badge: null
            },
            {
                title: "Facebook",
                path: '/recent-fb',
                icon: <FaIcons.FaGenderless style={{ marginLeft: '1rem'}} />,
                cName: 'nav-text',
                keyIndex: 2.2,
                badge: <Badge style={{marginLeft: '1rem'}} variant="success">Soon</Badge>
            },
            {
                title: "Instagram",
                path: '/recent-ig',
                icon: <FaIcons.FaGenderless style={{ marginLeft: '1rem'}} />,
                cName: 'nav-text',
                keyIndex: 2.3,
                badge: <Badge style={{marginLeft: '1rem'}} variant="success">Soon</Badge>
            }
        ],
        keyIndex: 4        
    }
]