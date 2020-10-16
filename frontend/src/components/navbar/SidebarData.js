import React from 'react';
import * as AiIcons from "react-icons/ai";
import * as BiIcons from "react-icons/bi";
import * as FaIcons from "react-icons/fa";
import * as TiIcons from "react-icons/ti";

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
        path: '/search',
        exactPath: false,
        icon: <BiIcons.BiSearchAlt />,
        cName: 'nav-text',
        dropDownList: [
            {
                title: 'Search Twitter',
                path: '/search-twitter',
                exactPath: false,
                icon: <TiIcons.TiMediaPlay style={{ marginLeft: '1rem'}} />,
                cName: 'nav-text',
            },
            {
                title: 'Search Facebook (soon)',
                path: '/search-fb',
                exactPath: false,
                icon: <TiIcons.TiMediaPlay style={{ marginLeft: '1rem'}} />,
                cName: 'nav-text',
            },
            {
                title: 'Search Instagram (soon)',
                path: '/search-ig',
                exactPath: false,
                icon: <TiIcons.TiMediaPlay style={{ marginLeft: '1rem'}} />,
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
        path: '/recentsearch',
        exactPath: false,
        icon: <FaIcons.FaChartBar />,
        cName: 'nav-text',
        dropDownList: [
            {
                title: 'Twitter',
                path: '/recent-twitter',
                exactPath: false,
                icon: <TiIcons.TiMediaPlay style={{ marginLeft: '1rem'}} />,
                cName: 'nav-text',
            },
            {
                title: 'Facebook (soon)',
                path: '/recent-fb',
                exactPath: false,
                icon: <TiIcons.TiMediaPlay style={{ marginLeft: '1rem'}} />,
                cName: 'nav-text',
            },
            {
                title: 'Instagram (soon)',
                path: '/recent-ig',
                exactPath: false,
                icon: <TiIcons.TiMediaPlay style={{ marginLeft: '1rem'}} />,
                cName: 'nav-text'
            }
        ]        
    }
]