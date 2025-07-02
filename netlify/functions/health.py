#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Функция проверки состояния сервера (health check)
"""

import json
from typing import Dict, Any


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Обработчик для проверки состояния сервера
    
    Args:
        event: Событие от Netlify
        context: Контекст выполнения
        
    Returns:
        Dict: HTTP ответ со статусом сервера
    """
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json; charset=utf-8',
            'Access-Control-Allow-Origin': '*',
            'Cache-Control': 'no-cache'
        },
        'body': json.dumps({
            'status': 'healthy',
            'service': 'MAX Weather Bot',
            'version': '1.0.0',
            'timestamp': context.aws_request_id if context else 'local'
        }, ensure_ascii=False)
    }