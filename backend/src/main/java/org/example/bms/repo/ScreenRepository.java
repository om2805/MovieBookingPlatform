package org.example.bms.repo;


import org.example.bms.model.Screen;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ScreenRepository extends JpaRepository<Screen,Long>
{
    List<Screen> findByTheaterId(Long theaterId);
}