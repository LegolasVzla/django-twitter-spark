import React, {useState} from 'react'
import Card from 'react-bootstrap/Card'
import ListGroup from 'react-bootstrap/ListGroup'
import Image from 'react-bootstrap/Image'
import * as FaIcons from "react-icons/fa";
import * as BiIcons from "react-icons/bs";
import * as moment from 'moment';
import Linkify from 'linkifyjs/react';
import Modal from 'react-bootstrap/Modal'
import Button from 'react-bootstrap/Button'
import {Link} from 'react-router-dom';

var options = {/* … */};

function CustomMessagesCard(props) {
    const cardItems = props.cardItems;
    const customTweetStyle = {
        margin: '0px 10px 0px 0px'
    };

    const [show, setShow] = useState(false);
  
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

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
                <Linkify options={options}>{item.tweet}</Linkify>
                </Card.Text>
                {/* Tweets Actions and Sentiment Analysis Resulting */}
                <span style={customTweetStyle}><FaIcons.FaRetweet style={{ color: "green" }}/>{' '}{item.retweets}</span>{' '}
                <span style={customTweetStyle}><FaIcons.FaRegHeart style={{ color: "red" }}/>{' '}{item.favorites}</span>{' '}
                <span style={customTweetStyle}><FaIcons.FaRegSmile style={{ color: "green" }}/>{' '}{Math.floor(item.positiveSentimentScore * 100)+'%'}</span>{' '}
                <span style={customTweetStyle}><FaIcons.FaRegFrown style={{ color: "red" }}/>{' '}{Math.floor(item.negativeSentimentScore * 100)+'%'}</span>{' '}
                <span style={customTweetStyle}><FaIcons.FaCrosshairs style={{ color: "blue" }}/>{' '}{Math.floor(item.confidenceScore * 100)+'%'}</span>{' '}
            </ListGroup.Item>
        </ListGroup>
    );

    return (
        <>
            <Card style={{ marginTop: '1rem', marginBottom: '1rem'}}>
            <Card.Header>
                <strong>{props.cardTitle} relacionados a su Búsqueda</strong>
                <Link to="#">
                    <BiIcons.BsInfoCircle style={{ marginLeft: '1rem '}} onClick={handleShow} />
                </Link>
            </Card.Header>
            <Card.Body>
                {tweetContent}
            </Card.Body>
            </Card>
            {/* Warning: findDOMNode is deprecated in StrictMode
            https://github.com/react-bootstrap/react-bootstrap/issues/5075 */}
            <Modal size="lg" show={show} onHide={handleClose}>
            <Modal.Header closeButton>
                <Modal.Title>Información sobre el Top de Tweets</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <p style={{textAlign: 'justify'}}>
                Estos tweets corresponden a una porción de los que fueron seleccionados y categorizados (positiva o negativamente según corresponda), como parte del Análisis de Sentimiento de su búsqueda. Los indicadores hacen referencia al porcentaje de que tan positiva <FaIcons.FaRegSmile style={{ color: "green" }}/> o negativamente <FaIcons.FaRegFrown style={{ color: "red" }}/> fueron catalogados de acuerdo a su contenido por nuestro algoritmo.<br/><br/>
                Adicionalmente se muestra el porcentaje de certeza o confiabilidad <FaIcons.FaCrosshairs style={{ color: "blue" }}/> que arrojó nuestro algoritmo con respecto a ese Tweet en particular.<br/><br/>
                Tenga en cuenta que nuestro algoritmo no es perfecto, por lo que podría presentar un porcentaje de error.
                </p>
            </Modal.Body>
                <img style={{width: '40rem', height: 'auto', alignSelf: 'center'}} src={require('../img/twitterSentimentAnalysisInfo.png')} alt="Twitter Sentiment Analysis Info"/> 
            <Modal.Footer>
                <Button variant="secondary" onClick={handleClose}>
                Cerrar
                </Button>
            </Modal.Footer>
            </Modal>
        </>
    )
}

export default CustomMessagesCard
