import React from 'react'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Container from 'react-bootstrap/Container'
import Card from 'react-bootstrap/Card'
import * as FaIcons from "react-icons/fa";
// import Jumbotron from 'react-bootstrap/Jumbotron'
import Tab from 'react-bootstrap/Tab'
import Nav from 'react-bootstrap/Nav'
import HomeTrend from '../components/HomeTrend'

function Home() {

    const homeCard = {
        marginTop: '1rem',
        borderRadius: '1rem',
        backgroundColor: 'rgba(0,0,0,.03)'
    };

    return (
        <Container>
            <Row>
                <Col xs={4} md={2}>

                </Col>
                <Col xs={10} md={8}>
                    <Card
                        style={homeCard}
                        className="mb-2"
                    >
                        <Card.Body>
                            <Card.Title><h3>El Analizador de Tópicos de Redes Sociales</h3></Card.Title>
                            <Card.Text style={{textAlign:'justify'}}>
                                <FaIcons.FaRegComment style={{marginRight: '0.5rem'}}/> Esta aplicación le permitirá realizar búsquedas sobre redes sociales, para saber si se está hablando bien o mal sobre una palabra buscada, mostrando estadísticas relacionadas a la misma a través del tiempo.
                            </Card.Text>
                        </Card.Body>
                    </Card>
                    <Card style={homeCard}>
                    <Card.Header style={{color: '#005C72'}}><FaIcons.FaBolt style={{marginRight: '0.5rem'}}/><strong>Tendencias y Opiniones</strong></Card.Header>
                    <Card.Body>
                        <Tab.Container id="left-tabs-example" defaultActiveKey="first">
                            <Nav variant="pills">
                                <Nav.Item>
                                <Nav.Link eventKey="first"><FaIcons.FaTwitter style={{marginRight: '0.5rem'}}/>Twitter</Nav.Link>
                                </Nav.Item>
                                <Nav.Item>
                                <Nav.Link eventKey="second"><FaIcons.FaFacebook style={{marginRight: '0.5rem'}}/>Facebook</Nav.Link>
                                </Nav.Item>
                                <Nav.Item>
                                <Nav.Link eventKey="third"><FaIcons.FaInstagram style={{marginRight: '0.5rem'}}/>Instagram</Nav.Link>
                                </Nav.Item>                                
                            </Nav>
                            <Tab.Content>
                                <Tab.Pane eventKey="first">
                                    <HomeTrend dataContent={true}/>
                                </Tab.Pane>
                                <Tab.Pane eventKey="second">
                                    <HomeTrend dataContent={false}/>
                                </Tab.Pane>
                                <Tab.Pane eventKey="third">
                                    <HomeTrend dataContent={false}/>
                                </Tab.Pane>                                
                            </Tab.Content>
                        </Tab.Container>
                    </Card.Body>
                    </Card>
                </Col>
                <Col xs={4} md={2}>
                </Col>
            </Row>
        </Container>        
    )
}

export default Home