import React from 'react'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Container from 'react-bootstrap/Container'
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import Card from 'react-bootstrap/Card'
import Breadcrumb from 'react-bootstrap/Breadcrumb'

function ProfileGet() {
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
                                <Breadcrumb.Item href="/profile-get" active>Ver Mi Perfil</Breadcrumb.Item>
                            </Breadcrumb>
                        </Card.Header>
                        <Card.Body>
                            <Card.Title><h3>Tu Perfil</h3></Card.Title>
                            <Card.Text>
                            <Form>
                                <Form.Group controlId="formGroupFirstName">
                                    <Form.Label>Nombre</Form.Label>
                                    <Form.Control type="text" placeholder="" readOnly />
                                </Form.Group>
                                <Form.Group controlId="formGroupLastName">
                                    <Form.Label>Apellido</Form.Label>
                                    <Form.Control type="text" placeholder="" readOnly />
                                </Form.Group>
                                <Form.Group controlId="formGroupEmail">
                                    <Form.Label>Email</Form.Label>
                                    <Form.Control placeholder="" readOnly type="email" />
                                </Form.Group>
                                <Button href="/profile-update" variant="primary" type="submit">
                                    Modificar Perfil
                                </Button>                        
                            </Form>
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

export default ProfileGet