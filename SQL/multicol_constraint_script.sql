ALTER TABLE mal_project.AnimeStudio
  ADD CONSTRAINT AnimeStudio UNIQUE(idAnime, idStudio);
  
ALTER TABLE mal_project.voicerole
  ADD CONSTRAINT voicerole UNIQUE(idPerson, idCharacter);
  
ALTER TABLE mal_project.staff
  ADD CONSTRAINT staff UNIQUE(idAnime, idPerson);