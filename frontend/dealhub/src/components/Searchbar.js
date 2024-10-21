"use client"
import { useState } from "react"
const isValidAmazonProductURL=(url)=>{
     try{
       const parsedURL=new URL(url);
       const hostname=parsedURL.hostname;

       if(
        hostname.includes('amazon.com')|| 
        hostname.includes('amazon.')
    ||hostname.endsWith('amazon')) {
        return true;
    }
     }catch(error){
       return false;
     }
}
const Searchbar=()=>{
    const[searchPrompt,setsearchPrompt]=useState('');
    const[isLoading,setisLoading]=useState(false);
    const handleSubmit=(event)=>{
        event.preventDefault();
        const isValidLink=isValidAmazonProductURL(searchPrompt)

        if(!isValidLink) return alert('please provide a valid amazon link')
        try{
        setisLoading(true);
        //scrape product here
    }  catch(error){
       console.log(error);
    }  finally{
        setisLoading(false);
    }
    }
    return(
        <form className="flex flex-wrap gap-4 mt-12"
        onSubmit={handleSubmit}>
            <input type="text"
            value={searchPrompt}
            onChange={(e)=>setsearchPrompt(e.target.value)}
            placeholder="enter product link"
            className="searchbar-input"/>
            
            <button type="submit" className="searchbar-btn"
            disabled={searchPrompt===''}>
               {isLoading? 'Searching...': 'Search'}
                </button>
        </form>

        
    )
}
export default Searchbar;