import React from 'react';
import * as AiIcons from "react-icons/ai";
import * as BiIcons from "react-icons/bi";
import * as FaIcons from "react-icons/fa";

export const TopSidebarData = [
    {
        title: 'Home',
        path: '/',
        icon: <AiIcons.AiFillHome />,
        cName: 'nav-text',
        dropDownList: []
    },
    {
        title: 'Buscar Palabras',
        path: '/search',
        icon: <BiIcons.BiSearchAlt />,
        cName: 'nav-text',
        dropDownList: [
            {
                title: 'Search Twitter',
                path: '/search-twitter',
                icon: <BiIcons.BiSearchAlt />,
                cName: 'nav-text',
            },
            {
                title: 'Search Facebook (soon)',
                path: '/search-fb',
                icon: <BiIcons.BiSearchAlt />,
                cName: 'nav-text',
            },
            {
                title: 'Search Instagram (soon)',
                path: '/search-ig',
                icon: <BiIcons.BiSearchAlt />,
                cName: 'nav-text'
            }
        ]
    },
    {
        title: 'Ver mi Diccionario',
        path: '/customdictionary',
        icon: <BiIcons.BiFile />,
        cName: 'nav-text',
        dropDownList: []
    }
]

export const BottomSidebarData = [
    {
        title: 'Buscar Recientes',
        path: '/recentsearch',
        icon: <FaIcons.FaChartBar />,
        cName: 'nav-text',
        dropDownList: [
            {
                title: 'Twitter',
                path: '/recent-twitter',
                icon: <BiIcons.BiSearchAlt />,
                cName: 'nav-text',
            },
            {
                title: 'Facebook (soon)',
                path: '/recent-fb',
                icon: <BiIcons.BiSearchAlt />,
                cName: 'nav-text',
            },
            {
                title: 'Instagram (soon)',
                path: '/recent-ig',
                icon: <BiIcons.BiSearchAlt />,
                cName: 'nav-text'
            }
        ]        
    }
]