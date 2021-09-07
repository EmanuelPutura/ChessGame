from errors.exceptions import RepositoryError


class MemoryRepository:
    def __init__(self):
        self._entities = []

    @property
    def entities(self):
        return self._entities

    def __len__(self):
        return len(self._entities)

    def search(self, entity):
        for mem_entity in self._entities:
            if mem_entity == entity:
                return mem_entity
        return None

    def insert(self, entity):
        if self.search(entity) is not None:
            raise RepositoryError('{} was already inserted into the repository.'.format(entity))
        self._entities.append(entity)

    def remove(self, entity):
        search_result = self.search(entity)
        if search_result is None:
            raise RepositoryError('{} was not found in the repository.'.format(entity))
        self._entities.remove(search_result)

    def update(self, entity, new_entity):
        for i in range(len(self._entities)):
            if self._entities[i] == entity:
                self._entities[i] = new_entity
                return
        raise RepositoryError('{} was not found in the repository.'.format(entity))
