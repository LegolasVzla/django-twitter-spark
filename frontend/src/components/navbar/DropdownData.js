import React from 'react';
import * as FaIcons from "react-icons/fa";
import * as FiIcons from "react-icons/fi";

export const DropdownData = [
    {
        title: 'Ver Mi Perfil',
        path: '/profile-get',
        exactPath: false,
        icon: <FaIcons.FaUser />,
        cName: 'nav-text'
    },
    {
        title: 'Cerrar Sesión',
        path: '/logout',
        exactPath: false,
        icon: <FiIcons.FiLogOut />,
        cName: 'nav-text'
    }
]
