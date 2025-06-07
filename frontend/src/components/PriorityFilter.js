import React from 'react';

const PriorityFilter = ({ onPriorityChange }) => {
    return (
        <select 
            onChange={(e) => onPriorityChange(e.target.value)}
            className="priority-filter"
        >
            <option value="">Todas las prioridades</option>
            <option value="alta">Alta</option>
            <option value="normal">Normal</option>
            <option value="baja">Baja</option>
        </select>
    );
};

export default PriorityFilter;