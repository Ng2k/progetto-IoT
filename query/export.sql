SELECT 
    s.mc_id,
    s.name AS stand_name, 
    st.name AS type, 
    e.name AS event_name,
    s.readings
FROM 
    "Stands" s
JOIN 
    "Stand Types" st ON s.type_id = st.id
JOIN 
    "Events" e ON s.event_id = e.id;