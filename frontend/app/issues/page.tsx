"use client";
import React from "react";
import './issues.css';
import Link from "next/link";
import Editor, { OnMount } from '@monaco-editor/react';
import { useRef } from 'react';

export default function IssuesPage() {
    const editorRef = useRef<monaco.editor.IStandaloneCodeEditor | null>(null);
    const [showSummary, setShowSummary] = React.useState(true);
    const handleEditorMount: OnMount = (editor, monaco) => {
        editorRef.current = editor;

        // Highlight lines on ide
        editor.deltaDecorations([], [
            {
                range: new monaco.Range(1, 1, 3, 1), // line 1 to 3
                options: {
                    isWholeLine: true,
                    className: 'highlight-line',
                },
            },
        ]);
    };
    return (
        <div
            className="min-h-screen relative"
            style={{
                background: 'radial-gradient(ellipse at center, #6B46C1 0%, #3B82F6 100%)',
                backgroundSize: '100% 100%'
            }}
        >
            {/* Navigation */}
            <nav className="absolute top-0 left-0 right-0 p-6 z-10">
                <div className="flex justify-between items-center">
                    {/*change link later*/}
                    <Link href="/issues/issue-name" style={{ textDecoration: 'none' }}>
                        <h1
                            className="text-white"
                            style={{
                                fontFamily: 'Montserrat, sans-serif',
                                fontWeight: 400,
                                fontSize: '60px',
                                lineHeight: '100%',
                                letterSpacing: '0%',
                            }}
                        >
                            Issue Name
                        </h1>
                    </Link>
                </div>
            </nav>

            {/* Search Input with exact specifications */}
            <div
                className="absolute"
                style={{ top: '21px', left: '769px' }}
            >
                <div className="glass-search-issues relative flex items-center">
                    <div className="absolute left-6 flex items-center pointer-events-none z-10">
                        <svg
                            className="w-6 h-6 text-gray-300"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth={2}
                                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                            />
                        </svg>
                    </div>
                    <input
                        type="text"
                        placeholder="Paste your issue link here"
                        className="w-full h-full pl-16 pr-6 text-white placeholder-gray-300 bg-transparent border-none outline-none relative z-10"
                        style={{
                            fontSize: '16px',
                        }}
                    />
                </div>
            </div>
            {/*landing page logo*/}
            <Link href="/" style={{ textDecoration: 'none' }}>
                <div className="glass-logo-feature absolute flex items-center"
                    style={{
                        top: '101px',
                        left: '1416px',
                    }}>
                </div>
            </Link>
            <div className="left-background-rectangle relative flex items-center"
                style={{
                    top: '117px',
                    left: '13px',
                }}>    </div>

            <div className="left-inner-rectangle relative flex items-center"
                style={{
                    top: '198px',
                    left: '13px',
                }}>    </div>

            {/* Summary section */}
            {showSummary && (
                <div
                    className="absolute flex items-start justify-start"
                    style={{
                        width: '498px',
                        height: '781px',
                        top: '218px',
                        left: '33px',
                        fontFamily: 'Montserrat, sans-serif',
                        fontWeight: 400,
                        fontSize: '24px',
                        lineHeight: '28px',
                        letterSpacing: '0%',
                        background: 'transparent',
                        backdropFilter: 'blur(20px)',
                        boxShadow: 'none',
                        borderRadius: '16px',
                        padding: '32px'
                    }}
                >
                    <span style={{ color: '#fff' }}>
                        {/* Your text goes here */}
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque euismod, urna eu tincidunt consectetur, nisi nisl aliquam nunc, eget aliquam massa nisl quis neque.
                    </span>
                </div>
            )}

            {/* Files section */}
            {!showSummary && (
                <div
                    className="absolute flex items-start justify-start"
                    style={{
                        width: '498px',
                        height: '781px',
                        top: '218px',
                        left: '33px',
                        fontFamily: 'Montserrat, sans-serif',
                        fontWeight: 400,
                        fontSize: '24px',
                        lineHeight: '28px',
                        letterSpacing: '0%',
                        background: 'transparent',
                        backdropFilter: 'blur(20px)',
                        boxShadow: 'none',
                        borderRadius: '16px',
                        padding: '32px'
                    }}
                >
                    <span style={{ color: '#fff' }}>
                        {/* Your text goes here */}
                        Files Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque euismod, urna eu tincidunt consectetur, nisi nisl aliquam nunc, eget aliquam massa nisl quis neque.
                    </span>
                </div>
            )}
            <div className="right-background-rectangle relative flex items-center"
                style={{
                    top: '117px',
                    left: '564px',
                }}>    </div>
            <div className="right-inner-rectangle relative flex items-center"
                style={{
                    top: '198px',
                    left: '564px',
                }}>    </div>
            {/* File logo (toggle summary) */}
            <div
                className="glass-logo-feature absolute flex items-center justify-center cursor-pointer"
                style={{
                    top: '128px',
                    left: '31px',
                    width: '61px',
                    height: '61px',
                    borderRadius: '50%',
                }}
                onClick={() => setShowSummary(true)}
            >
                {/* File SVG */}
                <svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="42" height="42">
                    <path d="M0 0 C3.41865168 1.81864319 5.56456983 4.03408009 8 7 C8.68231689 7.58096436 9.36463379 8.16192871 10.06762695 8.76049805 C12.51482853 11.59665472 12.50290747 13.04990671 12.49609375 16.75390625 C12.49673828 17.85541016 12.49738281 18.95691406 12.49804688 20.09179688 C12.47806641 21.23712891 12.45808594 22.38246094 12.4375 23.5625 C12.44458984 24.71169922 12.45167969 25.86089844 12.45898438 27.04492188 C12.39560074 35.36768042 12.39560074 35.36768042 10.85595703 37.82861328 C8.16173552 39.52907037 6.03932164 39.3718459 2.87109375 39.36328125 C1.67162109 39.36263672 0.47214844 39.36199219 -0.76367188 39.36132812 C-2.01728516 39.34521484 -3.27089844 39.32910156 -4.5625 39.3125 C-6.4487207 39.31733398 -6.4487207 39.31733398 -8.37304688 39.32226562 C-17.73311942 39.26688058 -17.73311942 39.26688058 -20 37 C-20.22406625 34.45449442 -20.32810413 32.02075208 -20.3359375 29.47265625 C-20.3425943 28.72793564 -20.3492511 27.98321503 -20.35610962 27.21592712 C-20.36624041 25.63982618 -20.37092651 24.0636823 -20.37060547 22.48754883 C-20.37497741 20.0749651 -20.41128472 17.66421276 -20.44921875 15.25195312 C-20.45508712 13.72136043 -20.45905638 12.19075904 -20.4609375 10.66015625 C-20.47530853 9.93820572 -20.48967957 9.21625519 -20.50448608 8.47242737 C-20.47503432 5.24630225 -20.43680861 3.47116899 -18.19677734 1.05493164 C-12.74524951 -1.5629892 -5.83781748 -0.82239095 0 0 Z M-15 5 C-15 14.57 -15 24.14 -15 34 C-7.74 34 -0.48 34 7 34 C7 27.73 7 21.46 7 15 C3.7 15 0.4 15 -3 15 C-3 11.7 -3 8.4 -3 5 C-6.96 5 -10.92 5 -15 5 Z " fill="#FFFFFF" transform="translate(25,1)" />
                    <path d="M0 0 C5.61 0 11.22 0 17 0 C17.33 1.32 17.66 2.64 18 4 C17 5 17 5 13.18359375 5.09765625 C11.60153318 5.09098089 10.01948841 5.07901875 8.4375 5.0625 C7.63119141 5.05798828 6.82488281 5.05347656 5.99414062 5.04882812 C3.99606244 5.03700518 1.99802217 5.01906914 0 5 C0 3.35 0 1.7 0 0 Z " fill="#FFFFFF" transform="translate(12,20)" />
                    <path d="M0 0 C5.61 0 11.22 0 17 0 C17.33 1.32 17.66 2.64 18 4 C17 5 17 5 13.40234375 5.09765625 C11.91403133 5.0909822 10.42573568 5.07902183 8.9375 5.0625 C8.17888672 5.05798828 7.42027344 5.05347656 6.63867188 5.04882812 C4.75908129 5.0370068 2.87953101 5.01907078 1 5 C0.67 3.35 0.34 1.7 0 0 Z " fill="#FFFFFF" transform="translate(12,27)" />
                    <path d="M0 0 C1.98 0 3.96 0 6 0 C6.5625 1.9375 6.5625 1.9375 7 4 C6 5 6 5 2.4375 5.0625 C1.303125 5.041875 0.16875 5.02125 -1 5 C-0.67 3.35 -0.34 1.7 0 0 Z " fill="#FFFFFF" transform="translate(13,13)" />
                </svg>
            </div>

            {/* Folder logo (toggle files) */}
            <div
                className="glass-logo-feature absolute flex items-center justify-center cursor-pointer"
                style={{
                    top: '128px',
                    left: '110px',
                    width: '61px',
                    height: '61px',
                    borderRadius: '50%',
                }}
                onClick={() => setShowSummary(false)}
            >
                {/* Folder SVG */}
                <svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="42" height="42">
                    <path d="M0 0 C1.71703125 -0.01546875 1.71703125 -0.01546875 3.46875 -0.03125 C4.4690625 0.1440625 5.469375 0.319375 6.5 0.5 C7.180625 1.48806641 7.180625 1.48806641 7.875 2.49609375 C9.48699537 4.95485081 9.48699537 4.95485081 13.40625 5.00390625 C14.93714124 5.04237752 16.46862598 5.06122172 18 5.0625 C25.92574949 5.10881072 25.92574949 5.10881072 28.21704102 6.66967773 C31.00116608 10.64162552 29.96619724 16.33017571 29.9375 21 C29.9674707 22.73056641 29.9674707 22.73056641 29.99804688 24.49609375 C29.99740234 25.60082031 29.99675781 26.70554687 29.99609375 27.84375 C29.99887329 29.36258789 29.99887329 29.36258789 30.00170898 30.91210938 C29.5 33.5 29.5 33.5 27.89477539 35.33081055 C24.70040878 36.8903805 22.23819991 36.87202565 18.6875 36.86328125 C18.03676514 36.86377975 17.38603027 36.86427826 16.71557617 36.86479187 C15.34388159 36.86245815 13.97218218 36.85277093 12.60058594 36.83618164 C10.50676995 36.81257632 8.41422792 36.81562686 6.3203125 36.82226562 C-5.13476577 36.77444455 -5.13476577 36.77444455 -8.5 34.5 C-10.77901824 29.94196352 -9.7301617 23.62921094 -9.75 18.625 C-9.770625 17.33207031 -9.79125 16.03914063 -9.8125 14.70703125 C-9.81765625 13.46566406 -9.8228125 12.22429688 -9.828125 10.9453125 C-9.8374707 9.80594238 -9.84681641 8.66657227 -9.85644531 7.49267578 C-9.08222595 0.99241486 -6.14134255 -0.05532741 0 0 Z M-4.5 5.5 C-4.52886751 9.64581887 -4.54675327 13.79161216 -4.5625 17.9375 C-4.57087891 19.12150391 -4.57925781 20.30550781 -4.58789062 21.52539062 C-4.59111328 22.65009766 -4.59433594 23.77480469 -4.59765625 24.93359375 C-4.60289307 25.97572021 -4.60812988 27.01784668 -4.61352539 28.09155273 C-4.77305556 30.45128747 -4.77305556 30.45128747 -3.5 31.5 C-1.42737924 31.58767112 0.64820294 31.60695873 2.72265625 31.59765625 C4.61274414 31.59282227 4.61274414 31.59282227 6.54101562 31.58789062 C7.88151109 31.57953403 9.22200588 31.57106907 10.5625 31.5625 C11.90689942 31.5574866 13.2513006 31.55292342 14.59570312 31.54882812 C17.89715433 31.53699497 21.1985826 31.51905886 24.5 31.5 C24.5 24.57 24.5 17.64 24.5 10.5 C19.0409214 10.32976028 19.0409214 10.32976028 13.58081055 10.20214844 C11.48735506 10.10828259 9.54242154 9.97927059 7.5 9.5 C7.01144531 8.82453125 6.52289063 8.1490625 6.01953125 7.453125 C5.51808594 6.80859375 5.01664063 6.1640625 4.5 5.5 C1.47596247 5.13378004 -1.46802279 5.27117153 -4.5 5.5 Z " fill="#F2F2F2" transform="translate(10.5,2.5)" />
                </svg>
            </div>

            <nav className="absolute flex items-center justify-center"
                style={{
                    width: '404px',
                    height: '52px',
                    top: '136px',
                    left: '586px',
                    borderWidth: '1px',
                    borderStyle: 'solid',
                    borderImageSource: 'conic-gradient(from 90deg at 0% 0%, rgba(255,255,255,0) -47.02deg, rgba(255,255,255,0.4) 42.98deg, rgba(255,255,255,0) 132.98deg, rgba(255,255,255,0.4) 222.98deg, rgba(255,255,255,0) 312.98deg, rgba(255,255,255,0.4) 402.98deg)',
                    fontFamily: 'Montserrat, sans-serif',
                    fontWeight: 400,
                    fontSize: '43px',
                    lineHeight: '100%',
                    letterSpacing: '0%',
                    textDecoration: 'none',
                    color: '#fff', // changed to white
                }}
            >
                <Link
                    href="/lorem/ipsum.json"
                    style={{
                        width: '100%',
                        height: '100%',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        textDecoration: 'none',
                        color: '#fff', // changed to white
                    }}
                >
                    ./lorem/ipsum.json
                </Link>
            </nav>

            <div
                className="absolute"
                style={{
                    top: '199px',
                    left: '565px',
                    width: '850px',
                    height: '806px',
                    borderRadius: '16px',
                    overflow: 'hidden',
                    boxShadow: '0 4px 32px 0 rgba(0,0,0,0.10)',
                    background: '#18181B',
                    display: 'flex',
                    flexDirection: 'column',
                }}
            >
                <Editor
                    height="90vh"
                    defaultLanguage="typescript" //change based on what the file type is 
                    defaultValue={`function greet(name: string) {\n  const msg = "Hello " + name;\n  return msg;\n}\n\ngreet("world");`}
                    theme="vs-dark"
                    onMount={handleEditorMount}
                    options={{
                        lineNumbers: 'on',
                        minimap: { enabled: false },
                    }}
                />
                <style jsx global>{`
                    .monaco-editor .highlight-line {
                    background-color: rgba(205, 205, 205, 0.1); 
                    border-left: 2px solid gray;
                    }
                    .monaco-editor .margin {
                    border-right: 1px solid #333; 
                    width: 60px !important;
                    }
                `
                }</style>
            </div>


        </div>
    );
}