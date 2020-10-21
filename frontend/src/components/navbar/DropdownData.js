import React from 'react';
import * as FaIcons from "react-icons/fa";
import * as FiIcons from "react-icons/fi";

export const DropdownData = [
    {
        title: 'Ver Mi Perfil',
        path: '/ver-perfil',
        exactPath: false,
        icon: <FaIcons.FaUser />,
        cName: 'nav-text'
    },
    {
        title: 'Cerrar Sesión',
        path: '/cerrar-sesion',
        exactPath: false,
        icon: <FiIcons.FiLogOut />,
        cName: 'nav-text'
    }
]
