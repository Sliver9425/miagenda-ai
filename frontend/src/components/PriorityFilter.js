import React from 'react';
import { Form } from 'react-bootstrap';

const PriorityFilter = ({ onPriorityChange }) => {
  return (
    <Form.Group className="mb-3 w-100" controlId="priorityFilter">
      <Form.Label>Filtrar por prioridad</Form.Label>
      <Form.Select onChange={(e) => onPriorityChange(e.target.value)}>
        <option value="">Todas las prioridades</option>
        <option value="alta">Alta</option>
        <option value="normal">Normal</option>
        <option value="baja">Baja</option>
      </Form.Select>
    </Form.Group>
  );
};

export default PriorityFilter;
