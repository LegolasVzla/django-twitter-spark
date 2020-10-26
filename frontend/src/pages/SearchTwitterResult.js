import React from 'react'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Container from 'react-bootstrap/Container'
import Card from 'react-bootstrap/Card'
import CustomSentimentCard from '../components/CustomSentimentCard'
import CustomTwitterActionsCard from '../components/CustomTwitterActionsCard'
import Breadcrumb from 'react-bootstrap/Breadcrumb'
import * as FaIcons from "react-icons/fa";

  const sentimentCardItems = [
    {
        cardType: 'Success',
        icon: <FaIcons.FaRegSmile style={{fontSize: '2rem'}} />,
        score: '60%',
        sentiment: 'Positive'
    },
    {
        cardType: 'Danger',
        icon: <FaIcons.FaRegFrown style={{fontSize: '2rem'}} />,
        score: '30%',
        sentiment: 'Negative'
    },
    {
        cardType: 'Secondary',
        icon: <FaIcons.FaRegMeh style={{fontSize: '2rem'}} />,
        score: '10%',
        sentiment: 'Neutral'
    }
];

const twitterActionsCardItems = [
    {
        cardType: 'Danger',
        icon: <FaIcons.FaRegHeart style={{fontSize: '4rem'}} />,
        action: 'Me Gusta',
        value: '150'
    },
    {
        cardType: 'Info',
        icon: <FaIcons.FaRetweet style={{fontSize: '4rem'}} />,
        action: 'Retweet',
        value: '50'
    }
];

function SearchTwitter() {
    return (
        <Container>
            <Row>
                <Col xs={4} md={2}>

                </Col>
                <Col xs={10} md={8}>
                    <Card style={{ marginTop: '1rem'}}>
                        <Card.Header>
                            <Breadcrumb>
                                <Breadcrumb.Item href="/">Home</Breadcrumb.Item>
                                <Breadcrumb.Item href="/search-twitter">Buscar en Twitter</Breadcrumb.Item>
                                <Breadcrumb.Item href="/search-twitter-result" active>Resultado de la Búsqueda</Breadcrumb.Item>
                            </Breadcrumb>
                        </Card.Header>
                        <Card.Body>
                            <Card.Title><h3>Resultado de su Búsqueda en Twitter</h3></Card.Title>
                            <Card.Text><FaIcons.FaRegComment/> Análisis de Sentimiento para la palabra:
                                <Row>
                                    <Col lg={true} style={{ marginTop: '1rem'}}>
                                        <CustomSentimentCard cardItems={sentimentCardItems[0]} />
                                        <CustomSentimentCard cardItems={sentimentCardItems[1]} />
                                        <CustomSentimentCard cardItems={sentimentCardItems[2]} />
                                    </Col>
                                    <Col lg={true} style={{ marginTop: '1rem'}}>
                                        <CustomTwitterActionsCard cardItems={twitterActionsCardItems[0]} />
                                        <CustomTwitterActionsCard cardItems={twitterActionsCardItems[1]} />
                                    </Col>
                                </Row>
                            </Card.Text>
                        </Card.Body>
                    </Card>

                </Col>
                <Col xs={4} md={2}>

                </Col>
            </Row>
        </Container>        
    )
}

export default SearchTwitter