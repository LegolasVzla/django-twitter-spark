import React from 'react'
import Card from 'react-bootstrap/Card'
import ListGroup from 'react-bootstrap/ListGroup'
import Image from 'react-bootstrap/Image'
import * as FaIcons from "react-icons/fa";
import * as moment from 'moment';

function CustomMessagesCard(props) {
    const cardItems = props.cardItems;
    const customTweetStyle = {
        margin: '0px 10px 0px 0px'
    };

    const tweetContent = cardItems.map((item,index) => 
        <ListGroup horizontal style={{ width: '100%' }} key={index}>
            {/* Twitter Account Images */}
            <ListGroup.Item style={{width: "5rem"}}>
                <Image src={item.profileImageUrl} roundedCircle />
            </ListGroup.Item>
            {/* Tweet Content */}
            <ListGroup.Item style={{width: "100%"}}>
                <Card.Subtitle className="mb-2 text-muted">
                    <strong>{item.account}</strong>{' '}
                    {moment(new Date(item.createdAt).toISOString()).fromNow()}
                </Card.Subtitle>
                <Card.Text>
                    {item.tweet}
                </Card.Text>
                {/* Tweets Actions and Sentiment Analysis Resulting */}
                <span style={customTweetStyle}><FaIcons.FaRetweet/>{' '}{item.retweets}</span>{' '}
                <span style={customTweetStyle}><FaIcons.FaRegHeart/>{' '}{item.favorites}</span>{' '}
                <span style={customTweetStyle}><FaIcons.FaRegSmile/>{' '}{Math.floor(item.positiveSentimentScore * 100)+'%'}</span>{' '}
                <span style={customTweetStyle}><FaIcons.FaRegFrown/>{' '}{Math.floor(item.negativeSentimentScore * 100)+'%'}</span>{' '}
                <span style={customTweetStyle}><FaIcons.FaCrosshairs/>{' '}{Math.floor(item.confidenceScore * 100)+'%'}</span>{' '}                
            </ListGroup.Item>
        </ListGroup>
    );

    return (
        <Card style={{ marginTop: '1rem', marginBottom: '1rem'}}>
        <Card.Header><strong>{props.cardTitle} relacionados a su Búsqueda</strong></Card.Header>
        <Card.Body>
            {tweetContent}
        </Card.Body>
        </Card>
    )
}

export default CustomMessagesCard
