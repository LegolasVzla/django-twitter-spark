import React from 'react'
import Card from 'react-bootstrap/Card'

function CustomTwitterActionsCard(props) {
    const cardItems = props.cardItems;

    return (
        <Card
            style={{ width: "18rem", display: 'flex', flexDirection: 'row'}}
            className="mb-2"
        >
            <Card
                bg={cardItems.cardType.toLowerCase()}
                style={{ width: "5rem", padding: '15px 0px 0px 8px'}}
                text={"white"}
            >
                {cardItems.icon}
            </Card>
            <Card
                bg={"light"}
                style={{ width: "13rem"}}
                text={"dark"}
            >
                <Card.Body>
                <Card.Title><strong>{cardItems.value}</strong></Card.Title>
                <Card.Text>
                    N° de {cardItems.action}
                </Card.Text>
                </Card.Body>
            </Card>
        </Card>
    )

}

  
export default CustomTwitterActionsCard
