package org.example.bms.service;

import lombok.RequiredArgsConstructor;
import org.example.bms.dto.TheaterDto;
import org.example.bms.exceptiom.ResourceNotFoundException;
import org.example.bms.model.Theater;
import org.example.bms.repo.TheaterRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class TheaterService {


    private final TheaterRepository theaterRepository;


    public TheaterDto createTheater(TheaterDto theaterDto)
    {
        Theater theater=mapToEntity(theaterDto);
        Theater savedTheater = theaterRepository.save(theater);
        return mapToDto(savedTheater);
    }

    public TheaterDto getTheaterById(Long id)
    {
        Theater theater=theaterRepository.findById(id)
                .orElseThrow(()-> new ResourceNotFoundException("Theater not found with id: "+id));
        return mapToDto(theater);
    }

    public List<TheaterDto> getAllTheaters()
    {
        List<Theater> theaters=theaterRepository.findAll();
        return theaters.stream()
                .map(this::mapToDto)
                .collect(Collectors.toList());
    }

    public List<TheaterDto> getAllTheaterByCity(String city)
    {
        List<Theater> theaters=theaterRepository.findByCity(city);
        return theaters.stream()
                .map(this::mapToDto)
                .collect(Collectors.toList());
    }

    //update theater
    public TheaterDto updateTheater(Long id,TheaterDto theaterDto){

        Theater theater = theaterRepository.findById(id)
                .orElseThrow(() ->
                        new ResourceNotFoundException(
                                "Theater not found with id: "
                                        + id));

        theater.setName(theaterDto.getName());
        theater.setAddress(theaterDto.getAddress());
        theater.setCity(theaterDto.getCity());
        theater.setTotalScreens(theaterDto.getTotalScreens());

        Theater updatedTheater = theaterRepository.save(theater);

        return mapToDto(updatedTheater);
    }

    //delete theater
    public  TheaterDto deleteTheater(Long id){

        Theater theater=theaterRepository.findById(id)
                .orElseThrow(()-> new ResourceNotFoundException("Theater not found with id: "+id));
        theaterRepository.delete(theater);
        return mapToDto(theater);
    }

    private TheaterDto mapToDto(Theater theater) {
        TheaterDto theaterDto=new TheaterDto();
        theaterDto.setId(theater.getId());
        theaterDto.setName(theater.getName());
        theaterDto.setCity(theater.getCity());
        theaterDto.setAddress(theater.getAddress());
        theaterDto.setTotalScreens(theater.getTotalScreens());
        return theaterDto;
    }

    private Theater mapToEntity(TheaterDto theaterDto) {
        Theater theater=new Theater();
        theater.setName(theaterDto.getName());
        theater.setAddress(theaterDto.getAddress());
        theater.setCity(theaterDto.getCity());
        theater.setTotalScreens(theaterDto.getTotalScreens());
        return theater;
    }
}