import React from 'react';
import * as AiIcons from "react-icons/ai";
import * as BiIcons from "react-icons/bi";
import * as FaIcons from "react-icons/fa";
import Badge from 'react-bootstrap/Badge'

export const TopSidebarData = [
    {
        title: 'Home',
        path: '/',
        exactPath: true,
        icon: <AiIcons.AiFillHome />,
        cName: 'nav-text',
        dropDownList: []
    },
    {
        title: 'Buscar Palabras',
        path: '#',
        exactPath: false,
        icon: <BiIcons.BiSearchAlt />,
        cName: 'nav-text',
        dropDownList: [
            {
                title: 'Twitter',
                path: '/search-twitter',
                exactPath: false,
                icon: <FaIcons.FaGenderless style={{ marginLeft: '1rem'}} />,
                cName: 'nav-text',
            },
            {
                title: ["Facebook",<Badge variant="success">Soon</Badge>],
                path: '/search-fb',
                exactPath: false,
                icon: <FaIcons.FaGenderless style={{ marginLeft: '1rem'}} />,
                cName: 'nav-text',
            },
            {
                title: ["Instagram",<Badge variant="success">Soon</Badge>],
                path: '/search-ig',
                exactPath: false,
                icon: <FaIcons.FaGenderless style={{ marginLeft: '1rem'}} />,
                cName: 'nav-text'
            }
        ]
    },
    {
        title: 'Ver mi Diccionario',
        path: '/customdictionary',
        exactPath: false,
        icon: <BiIcons.BiFile />,
        cName: 'nav-text',
        dropDownList: []
    }
]

export const BottomSidebarData = [
    {
        title: 'Buscar Recientes',
        path: '#',
        exactPath: false,
        icon: <FaIcons.FaChartBar />,
        cName: 'nav-text',
        dropDownList: [
            {
                title: 'Twitter',
                path: '/recent-twitter',
                exactPath: false,
                icon: <FaIcons.FaGenderless style={{ marginLeft: '1rem'}} />,
                cName: 'nav-text',
            },
            {
                title: ["Facebook",<Badge variant="success">Soon</Badge>],
                path: '/recent-fb',
                exactPath: false,
                icon: <FaIcons.FaGenderless style={{ marginLeft: '1rem'}} />,
                cName: 'nav-text',
            },
            {
                title: ["Instagram",<Badge variant="success">Soon</Badge>],
                path: '/recent-ig',
                exactPath: false,
                icon: <FaIcons.FaGenderless style={{ marginLeft: '1rem'}} />,
                cName: 'nav-text'
            }
        ]        
    }
]