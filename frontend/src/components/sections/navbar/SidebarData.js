import React from 'react'
import * as AiIcons from "react-icons/ai";
import * as BiIcons from "react-icons/bi";
import * as FaIcons from "react-icons/fa";

export const SidebarData = [
    {
        title: 'Home',
        path: '/',
        icon: <AiIcons.AiFillHome />,
        cName: 'nav-text'

    },
    {
        title: 'Buscar Palabras',
        path: '/search',
        icon: <BiIcons.BiSearchAlt />,
        cName: 'nav-text'

    },
    {
        title: 'Ver mi Diccionario',
        path: '/customdictionary',
        icon: <BiIcons.BiFile />,
        cName: 'nav-text'

    },
    {
        title: 'Buscar Recientes',
        path: '/recentsearch',
        icon: <FaIcons.FaChartBar />,
        cName: 'nav-text'

    },
]