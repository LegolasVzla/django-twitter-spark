import React, {useState} from 'react'
import cn from 'classnames';

function Submenu(props) {
    const [toggle, setToggle] = useState(false);
    const items = props.subMenuItems;

    const subMenuItems = items.map((item,index) =>
        <li key={index.toString()} className="item">{item.title}</li>
    );

    function toggleSubMenu() {
        setToggle(!toggle);
    }

    const classes = cn('menu',{'transition': toggle,'visible': toggle});

    return (
        <div className="ui dropdown item" onClick={toggleSubMenu}>
            <i className="dropdown icon" />
                <ul className={classes}>
                    {subMenuItems}
                </ul>
        </div>
    )
}

export default Submenu
