import React from 'react'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Card from 'react-bootstrap/Card'
import * as FaIcons from "react-icons/fa";

function HomeTrend(props) {

    const homeCardStyle = {
        marginTop: '1rem',
        borderRadius: '1rem',
        backgroundColor: 'rgba(0,0,0,.03)'
    };

    return (
        <div>
            <Card style={homeCardStyle}>
                <Card.Body>
                    <Card.Title>Nuestra Nube de Palabras</Card.Title>
                        {props.dataContent ? (
                            <Row>
                                <Col lg={true} style={{ marginTop: '1rem'}}>
                                </Col>
                            </Row>
                        ) : (
                            <div style={{textAlign:'center'}}><FaIcons.FaCogs style={{fontSize: '5rem',marginRight: '0.5rem'}}/>En Construcción</div>
                        )}
                </Card.Body>
            </Card>
            <Card style={homeCardStyle}>
                <Card.Body>
                    <Card.Title>Nuestros Tópicos</Card.Title>
                        {props.dataContent ? (
                            <Row>
                                <Col lg={true} style={{ marginTop: '1rem'}}>
                                </Col>
                            </Row>
                        ) : (
                            <div style={{textAlign:'center'}}><FaIcons.FaCogs style={{fontSize: '5rem',marginRight: '0.5rem'}}/>En Construcción</div>
                        )}
                </Card.Body>
            </Card>
        </div>
    )
}

export default HomeTrend
