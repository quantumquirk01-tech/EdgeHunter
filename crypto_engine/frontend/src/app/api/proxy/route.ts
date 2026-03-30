
import { NextResponse } from 'next/server';

export async function GET() {
  const backendUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://89.45.45.164:8001/api/v1';
  
  try {
    const response = await fetch(`${backendUrl}/trades/recent`, {
      cache: 'no-store',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    if (!response.ok) {
      throw new Error(`Backend returned ${response.status}`);
    }
    
    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Proxy fetch failed:', error);
    return NextResponse.json({ error: 'Failed to fetch signals from backend' }, { status: 500 });
  }
}
