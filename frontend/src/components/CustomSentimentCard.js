import React from 'react'
import Card from 'react-bootstrap/Card'

function CustomSentimentCard(props) {
    const cardItems = props.cardItems;

    return (
        <Card
            bg={cardItems.cardType.toLowerCase()}
            text={"white"}
            style={{ width: "18rem" }}
            className="mb-2"
        >
            <Card.Header>{cardItems.icon}{'  '}{cardItems.score}{' '}{cardItems.sentiment}</Card.Header>
        </Card>
    )

}

  
export default CustomSentimentCard
