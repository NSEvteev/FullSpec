/**
 * Unit Test Example
 *
 * Источник: /.claude/instructions/tests/unit.md
 *
 * Эталонный пример unit-теста, соответствующий всем стандартам проекта:
 * - Паттерн AAA (Arrange-Act-Assert)
 * - Формат naming: "should {behavior} when {condition}"
 * - Изоляция через beforeEach
 * - Один assert на тест
 */

import { describe, it, expect, beforeEach, jest } from '@jest/globals';

// ============================================================================
// Тестируемый модуль (пример)
// ============================================================================

interface Token {
  value: string;
  expiresAt: number;
}

class TokenValidator {
  validate(token: string | null): boolean {
    if (!token || token === '') {
      return false;
    }
    // Простая валидация для примера
    return token.startsWith('valid-');
  }

  isExpired(token: Token): boolean {
    return Date.now() > token.expiresAt;
  }
}

// ============================================================================
// Тесты
// ============================================================================

describe('TokenValidator', () => {
  let validator: TokenValidator;

  // Стандарт: beforeEach для изоляции тестов
  beforeEach(() => {
    validator = new TokenValidator();
    jest.clearAllMocks();
  });

  // Стандарт: describe для группировки по методу
  describe('validate', () => {
    // Стандарт: формат "should {behavior} when {condition}"
    it('should return true when token is valid', () => {
      // Arrange (подготовка)
      const token = 'valid-token-123';

      // Act (действие)
      const result = validator.validate(token);

      // Assert (проверка) - один assert на тест
      expect(result).toBe(true);
    });

    // Стандарт: edge cases в отдельных тестах
    it('should return false when token is empty', () => {
      // Arrange
      const token = '';

      // Act
      const result = validator.validate(token);

      // Assert
      expect(result).toBe(false);
    });

    it('should return false when token is null', () => {
      // Arrange
      const token = null;

      // Act
      const result = validator.validate(token);

      // Assert
      expect(result).toBe(false);
    });

    it('should return false when token does not start with valid-', () => {
      // Arrange
      const token = 'invalid-token';

      // Act
      const result = validator.validate(token);

      // Assert
      expect(result).toBe(false);
    });
  });

  describe('isExpired', () => {
    // Стандарт: детерминированность через фиксированное время
    it('should return false when token is not expired', () => {
      // Arrange - фиксируем время
      jest.useFakeTimers();
      jest.setSystemTime(new Date('2024-01-15T00:00:00Z'));

      const token: Token = {
        value: 'valid-token',
        expiresAt: new Date('2024-01-16T00:00:00Z').getTime(),
      };

      // Act
      const result = validator.isExpired(token);

      // Assert
      expect(result).toBe(false);

      // Cleanup
      jest.useRealTimers();
    });

    it('should return true when token is expired', () => {
      // Arrange
      jest.useFakeTimers();
      jest.setSystemTime(new Date('2024-01-17T00:00:00Z'));

      const token: Token = {
        value: 'valid-token',
        expiresAt: new Date('2024-01-16T00:00:00Z').getTime(),
      };

      // Act
      const result = validator.isExpired(token);

      // Assert
      expect(result).toBe(true);

      // Cleanup
      jest.useRealTimers();
    });
  });
});

// ============================================================================
// Пример с моками внешних зависимостей
// ============================================================================

interface UserRepository {
  findById(id: string): Promise<{ id: string; name: string } | null>;
}

class UserService {
  constructor(private readonly repository: UserRepository) {}

  async getUserName(userId: string): Promise<string> {
    const user = await this.repository.findById(userId);
    if (!user) {
      throw new Error('User not found');
    }
    return user.name;
  }
}

describe('UserService', () => {
  let service: UserService;
  let mockRepository: jest.Mocked<UserRepository>;

  beforeEach(() => {
    // Стандарт: мокаем только внешние зависимости
    mockRepository = {
      findById: jest.fn(),
    };
    service = new UserService(mockRepository);
    jest.clearAllMocks();
  });

  describe('getUserName', () => {
    it('should return user name when user exists', async () => {
      // Arrange
      const userId = 'user-123';
      const mockUser = { id: userId, name: 'John Doe' };
      mockRepository.findById.mockResolvedValue(mockUser);

      // Act
      const result = await service.getUserName(userId);

      // Assert
      expect(result).toBe('John Doe');
      expect(mockRepository.findById).toHaveBeenCalledWith(userId);
    });

    it('should throw error when user not found', async () => {
      // Arrange
      const userId = 'non-existent';
      mockRepository.findById.mockResolvedValue(null);

      // Act & Assert
      await expect(service.getUserName(userId)).rejects.toThrow('User not found');
    });
  });
});
