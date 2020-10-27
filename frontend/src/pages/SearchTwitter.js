import React from 'react'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Container from 'react-bootstrap/Container'
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import Card from 'react-bootstrap/Card'
import Breadcrumb from 'react-bootstrap/Breadcrumb'
import * as FaIcons from "react-icons/fa";

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
                                <Breadcrumb.Item href="/search-twitter" active>Buscar en Twitter</Breadcrumb.Item>
                            </Breadcrumb>
                        </Card.Header>
                        <Card.Body>
                            <Card.Title><h3>Buscar en Twitter</h3></Card.Title>
                            <Card.Text>
                                <FaIcons.FaRegComment/> Ingresa una palabra para mostrar el tópico obtenido y también para saber si están hablando bien o mal sobre la misma.
                            </Card.Text>
                            <Form>
                                <Form.Group controlId="formBasicEmail" style={{marginTop: '1rem'}}>
                                    <Form.Control type="email"/>
                                </Form.Group>
                                <Button href="/search-twitter-result" variant="primary" type="submit">
                                    Buscar
                                </Button>                        
                            </Form>
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